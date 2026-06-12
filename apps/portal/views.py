from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .registry import SECTIONS, get_section


def _model_field_names(model):
    return [f.name for f in model._meta.fields]


def _build_form(model, exclude=None):
    exclude = exclude or []
    safe_exclude = set(exclude) | {'password', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'groups', 'user_permissions'}

    class DynamicModelForm(forms.ModelForm):
        class Meta:
            model = model
            fields = '__all__'
            exclude = list(safe_exclude)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.setdefault('class', 'checkbox')
                else:
                    field.widget.attrs.setdefault('class', 'input')

    return DynamicModelForm


def _format_value(obj, field_name):
    if obj is None:
        return '—'
    try:
        value = getattr(obj, field_name)
    except AttributeError:
        return '—'
    if value is None or value == '':
        return '—'
    if hasattr(value, 'get_status_display'):
        return value.get_status_display()
    if hasattr(value, 'get_tipo_display'):
        return value.get_tipo_display()
    if hasattr(value, 'get_metodo_display'):
        return value.get_metodo_display()
    if field_name == 'aberta':
        return 'Sim' if value else 'Não'
    if field_name == 'is_active':
        return 'Sim' if value else 'Não'
    return str(value)


class HomeView(View):
    def get(self, request):
        counts = []
        for section in SECTIONS:
            model = section['model']
            counts.append(
                {
                    **section,
                    'count': model.objects.count(),
                }
            )
        return render(
            request,
            'portal/home.html',
            {
                'sections': counts,
                'total_models': len(SECTIONS),
            },
        )


class ArquiteturaView(View):
    def get(self, request):
        return render(request, 'portal/arquitetura.html', {'sections': SECTIONS})


class ModelListView(View):
    def get(self, request, slug):
        section = get_section(slug)
        if not section:
            return render(request, 'portal/404_section.html', status=404)

        model = section['model']
        items = model.objects.all()
        rows = []
        for item in items:
            rows.append(
                {
                    'obj': item,
                    'cells': [_format_value(item, f) for f in section['list_fields']],
                }
            )

        return render(
            request,
            'portal/list.html',
            {
                'section': section,
                'rows': rows,
                'fields': section['list_fields'],
            },
        )


class ModelDetailView(View):
    def get(self, request, slug, pk):
        section = get_section(slug)
        if not section:
            return render(request, 'portal/404_section.html', status=404)

        model = section['model']
        obj = get_object_or_404(model, pk=pk)
        field_rows = []
        for name in _model_field_names(model):
            field_rows.append({'name': name, 'value': _format_value(obj, name)})

        return render(
            request,
            'portal/detail.html',
            {
                'section': section,
                'obj': obj,
                'field_rows': field_rows,
            },
        )


class ModelCreateView(View):
    def get(self, request, slug):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        form_class = _build_form(section['model'], section['form_exclude'])
        return render(
            request,
            'portal/form.html',
            {
                'section': section,
                'form': form_class(),
                'action': 'create',
            },
        )

    def post(self, request, slug):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        form_class = _build_form(section['model'], section['form_exclude'])
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'{section["title"]} criado(a) com sucesso.')
            return redirect('portal:detail', slug=slug, pk=obj.pk)

        return render(
            request,
            'portal/form.html',
            {
                'section': section,
                'form': form,
                'action': 'create',
            },
        )


class ModelUpdateView(View):
    def get(self, request, slug, pk):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        obj = get_object_or_404(section['model'], pk=pk)
        form_class = _build_form(section['model'], section['form_exclude'])
        return render(
            request,
            'portal/form.html',
            {
                'section': section,
                'form': form_class(instance=obj),
                'action': 'edit',
                'obj': obj,
            },
        )

    def post(self, request, slug, pk):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        obj = get_object_or_404(section['model'], pk=pk)
        form_class = _build_form(section['model'], section['form_exclude'])
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'{section["title"]} atualizado(a) com sucesso.')
            return redirect('portal:detail', slug=slug, pk=obj.pk)

        return render(
            request,
            'portal/form.html',
            {
                'section': section,
                'form': form,
                'action': 'edit',
                'obj': obj,
            },
        )


class ModelDeleteView(View):
    def get(self, request, slug, pk):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        obj = get_object_or_404(section['model'], pk=pk)
        return render(
            request,
            'portal/delete_confirm.html',
            {'section': section, 'obj': obj},
        )

    def post(self, request, slug, pk):
        section = get_section(slug)
        if not section or not section['allow_crud']:
            return redirect('portal:home')

        obj = get_object_or_404(section['model'], pk=pk)
        try:
            obj.delete()
            messages.success(request, f'{section["title"]} excluído(a) com sucesso.')
        except Exception as exc:
            messages.error(request, f'Não foi possível excluir: {exc}')
            return redirect('portal:detail', slug=slug, pk=pk)

        return redirect('portal:list', slug=slug)
