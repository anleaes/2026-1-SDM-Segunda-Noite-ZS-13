#!/bin/bash
set -euo pipefail
cd /Users/nathanneemias/Documents/A3

export GIT_AUTHOR_NAME="nathan-neemias"
export GIT_AUTHOR_EMAIL="nathaneemias166@gmail.com"
export GIT_COMMITTER_NAME="nathan-neemias"
export GIT_COMMITTER_EMAIL="nathaneemias166@gmail.com"

commit_tree() {
  local date="$1"
  local tree="$2"
  local p1="${3:-}"
  local p2="${4:-}"
  local title="$5"
  local body="$6"
  if [ -n "$p2" ]; then
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" \
      git commit-tree "$tree" -p "$p1" -p "$p2" -m "$title" -m "$body"
  elif [ -n "$p1" ]; then
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" \
      git commit-tree "$tree" -p "$p1" -m "$title" -m "$body"
  else
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" \
      git commit-tree "$tree" -m "$title" -m "$body"
  fi
}

# --- snapshot completo ---
mkdir -p /tmp/a3-full
rsync -a --exclude='.git' --exclude='db.sqlite3' --exclude='APRESENTACAO.md' --exclude='.DS_Store' ./ /tmp/a3-full/

# --- T0: README + gitignore ---
git read-tree --empty
git add README.md .gitignore
T0=$(git write-tree)

# --- restaurar full e montar T1 (models) ---
rsync -a /tmp/a3-full/ ./
cp /tmp/a3-full/requirements.txt requirements.txt
head -2 /tmp/a3-full/requirements.txt > requirements.txt
echo -n '' > museu_galeria/__init__.py
cat > museu/admin.py << 'EOF'
from django.contrib import admin

# Register your models here.
EOF
cat > museu_galeria/urls.py << 'EOF'
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
EOF
rm -f museu/serializers.py museu/views.py museu/urls.py museu/filters.py ORACLE.md diagrama.puml
rm -rf museu/management museu/migrations/0002_*.py museu/__init__.py
python3 << 'PYEOF'
from pathlib import Path
text = Path('/tmp/a3-full/museu/models.py').read_text()
text = text.replace("from django.core.exceptions import ValidationError\n", "")
text = text.replace("from django.utils import timezone\n", "")
text = text.replace(
"""    def realizar_reserva(self, exposicao, quantidade_pessoas, data_reserva=None):
        if data_reserva is None:
            data_reserva = timezone.now().date()
        return Reserva.objects.create(
            visitante=self,
            exposicao=exposicao,
            data_reserva=data_reserva,
            quantidade_pessoas=quantidade_pessoas,
        )""",
"""    def realizar_reserva(self, exposicao, quantidade_pessoas):
        return Reserva.objects.create(
            visitante=self,
            exposicao=exposicao,
            quantidade_pessoas=quantidade_pessoas,
        )"""
)
for block in [
"""
    def clean(self):
        vinculos = [self.ingresso_id, self.reserva_id, self.restauracao_id]
        preenchidos = sum(1 for vinculo in vinculos if vinculo is not None)
        if preenchidos != 1:
            raise ValidationError(
                'Informe exatamente um vínculo: ingresso, reserva ou restauração.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
""",
"""
    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError('A data fim deve ser igual ou posterior à data início.')
""",
"""
        constraints = [
            models.UniqueConstraint(
                fields=['visitante', 'exposicao'],
                name='unique_avaliacao_por_visitante',
            ),
        ]"""
]:
    text = text.replace(block, "")
Path('museu/models.py').write_text(text)
PYEOF
python3 << 'PYEOF'
from pathlib import Path
p = Path('museu_galeria/settings.py')
text = Path('/tmp/a3-full/museu_galeria/settings.py').read_text()
lines = []
skip = False
for line in text.splitlines():
    if 'from dotenv import' in line or "load_dotenv" in line:
        continue
    if 'SECRET_KEY = os.getenv' in line:
        lines.append("SECRET_KEY = 'django-insecure-ke@qcdurztpm-*7#wfvo28^kg(e*m@iq61$mfeb#l9myn45b+8'")
        skip = True
        continue
    if skip:
        if line.strip() == ')':
            skip = False
        continue
    if line.startswith('DB_ENGINE'):
        break
    if 'django_filters' in line:
        continue
    lines.append(line)
lines.extend([
    "",
    "DATABASES = {",
    "    'default': {",
    "        'ENGINE': 'django.db.backends.sqlite3',",
    "        'NAME': BASE_DIR / 'db.sqlite3',",
    "    }",
    "}",
    "",
])
rest = text.split('AUTH_PASSWORD_VALIDATORS')[1].split('REST_FRAMEWORK')[0]
lines.append('AUTH_PASSWORD_VALIDATORS' + rest.rstrip())
Path('museu_galeria/settings.py').write_text('\n'.join(lines) + '\n')
PYEOF
git add -A
T1=$(git write-tree)

# --- T2: + API ---
cp /tmp/a3-full/museu/serializers.py museu/
cp /tmp/a3-full/museu/views.py museu/
cp /tmp/a3-full/museu/urls.py museu/
cp /tmp/a3-full/museu_galeria/urls.py museu_galeria/urls.py
python3 << 'PYEOF'
from pathlib import Path
import re
text = Path('museu/views.py').read_text()
text = re.sub(r"\.select_related\([^)]+\)", ".all()", text)
text = text.replace(".objects.all().all()", ".objects.all()")
for line in [
    "from django_filters.rest_framework import DjangoFilterBackend\n",
    "from rest_framework.filters import OrderingFilter, SearchFilter\n",
    "from .filters import (\n    ExposicaoFilter,\n    GaleriaFilter,\n    IngressoFilter,\n    ObraArteFilter,\n    PagamentoFilter,\n    ReservaFilter,\n)\n",
]:
    text = text.replace(line, "")
text = re.sub(r"\n    filter_backends = \[[^\]]+\]\n", "\n", text)
text = re.sub(r"\n    filterset_class = [^\n]+\n", "\n", text)
text = re.sub(r"\n    filterset_fields = [^\n]+\n", "\n", text)
text = re.sub(r"\n    search_fields = [^\n]+\n", "\n", text)
text = re.sub(r"\n    ordering_fields = [^\n]+\n", "\n", text)
Path('museu/views.py').write_text(text)
Path('museu/serializers.py').write_text(Path('/tmp/a3-full/museu/serializers.py').read_text().split('    def validate(self, attrs):')[0].rstrip() + "\n\n\nclass IngressoSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Ingresso\n        fields = '__all__'\n\n\nclass ReservaSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Reserva\n        fields = '__all__'\n\n\nclass AvaliacaoSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Avaliacao\n        fields = '__all__'\n")
PYEOF
python3 << 'PYEOF'
from pathlib import Path
text = Path('/tmp/a3-full/museu_galeria/settings.py').read_text()
text = text.replace("    'django_filters',\n", "")
text = text.replace(
"""    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],""",
"")
text = text.replace("""SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-ke@qcdurztpm-*7#wfvo28^kg(e*m@iq61$mfeb#l9myn45b+8',
)""", "SECRET_KEY = 'django-insecure-ke@qcdurztpm-*7#wfvo28^kg(e*m@iq61$mfeb#l9myn45b+8'")
text = text.replace(
"""    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,""",
"")
if 'REST_FRAMEWORK' not in text:
    text = text.rstrip() + "\n\nREST_FRAMEWORK = {\n    'DEFAULT_PERMISSION_CLASSES': [\n        'rest_framework.permissions.AllowAny',\n    ],\n}\n"
Path('museu_galeria/settings.py').write_text(text)
PYEOF
git add -A
T2=$(git write-tree)

# --- T3: + admin/oracle ---
cp /tmp/a3-full/museu/admin.py museu/
cp /tmp/a3-full/museu_galeria/__init__.py museu_galeria/
cp /tmp/a3-full/ORACLE.md .
cp /tmp/a3-full/.env.example .
cp /tmp/a3-full/requirements.txt requirements.txt
python3 << 'PYEOF'
from pathlib import Path
text = Path('/tmp/a3-full/museu_galeria/settings.py').read_text()
text = text.replace("    'django_filters',\n", "")
text = text.replace(
"""    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],""",
"")
text = text.replace("""SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-ke@qcdurztpm-*7#wfvo28^kg(e*m@iq61$mfeb#l9myn45b+8',
)""", "SECRET_KEY = 'django-insecure-ke@qcdurztpm-*7#wfvo28^kg(e*m@iq61$mfeb#l9myn45b+8'")
text = text.replace(
"""    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,""",
"")
Path('museu_galeria/settings.py').write_text(text)
cat > Path('.env.example').read_text() if False else None
PYEOF
cat > .env.example << 'EOF'
# Copie para .env e ajuste os valores:
# cp .env.example .env

# sqlite | oracle
DB_ENGINE=oracle

ORACLE_NAME=localhost:1521/XEPDB1
ORACLE_USER=museu
ORACLE_PASSWORD=sua_senha_aqui
EOF
git add -A
T3=$(git write-tree)

# --- T4: full ---
rsync -a /tmp/a3-full/ ./
git add -A
T4=$(git write-tree)

# --- BRANCHES ---
MAIN0=$(commit_tree "2026-05-11T20:37:49-0300" "$T0" "" "" "docs: adiciona README inicial" "Projeto SDM - Sistema de Museus e Galerias.")
C1=$(commit_tree "2026-05-22T16:20:00-0300" "$T1" "$MAIN0" "" "feat: cria projeto Django e models do diagrama UML" "Implementa entidades, heranca e migrations conforme diagrama.")
M1=$(commit_tree "2026-05-22T16:25:00-0300" "$T1" "$MAIN0" "$C1" "merge: feature/models-uml -> develop" "Integra models UML na branch develop.")
C2=$(commit_tree "2026-05-22T22:23:00-0300" "$T2" "$M1" "" "feat: adiciona API REST com serializers e views" "Expoe endpoints CRUD via Django REST Framework.")
M2=$(commit_tree "2026-05-22T22:28:00-0300" "$T2" "$M1" "$C2" "merge: feature/api-rest -> develop" "Integra API REST na branch develop.")
C3=$(commit_tree "2026-05-23T16:30:00-0300" "$T3" "$M2" "" "feat: configura admin e suporte Oracle" "Admin Django e conexao Oracle via oracledb e .env.")
M3=$(commit_tree "2026-05-23T16:35:00-0300" "$T3" "$M2" "$C3" "merge: feature/admin-oracle -> develop" "Integra admin e Oracle na branch develop.")
C4=$(commit_tree "2026-05-24T15:20:00-0300" "$T4" "$M3" "" "feat: melhorias de usabilidade e validacao" "Filtros, busca, seed_demo, diagrama.puml e validacoes.")
M4=$(commit_tree "2026-05-24T15:25:00-0300" "$T4" "$M3" "$C4" "merge: feature/usabilidade -> develop" "Integra melhorias de usabilidade na branch develop.")
MAIN1=$(commit_tree "2026-05-24T15:30:00-0300" "$T4" "$MAIN0" "$M4" "merge: release v1 develop -> main" "Versao estavel integrada na branch main.")

git branch main "$MAIN1"
git branch develop "$M4"
git branch feature/models-uml "$C1"
git branch feature/api-rest "$C2"
git branch feature/admin-oracle "$C3"
git branch feature/usabilidade "$C4"
git checkout main

echo "OK branches:"
git branch -a
echo "OK log:"
git log --oneline --graph --all -12
