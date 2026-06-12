# Categorias — fluxo completo (React Native + Django)

CRUD de **CategoriaObra**: listar, adicionar, editar e excluir.  
Foco no **código principal** — sem imports, estilos ou detalhes de infra.

---

## Visão geral

```
categorias.tsx  →  services.ts  →  HTTP  →  urls.py  →  views.py  →  serializer  →  model  →  banco
```

| Ação no app | HTTP | URL | Backend (DRF) |
|-------------|------|-----|---------------|
| Abrir tela / atualizar | GET | `/api/categorias-obra/` | `list()` |
| + Nova → Salvar | POST | `/api/categorias-obra/` | `create()` |
| Editar → Salvar | PATCH | `/api/categorias-obra/{id}/` | `partial_update()` |
| Excluir | DELETE | `/api/categorias-obra/{id}/` | `destroy()` |

### Arquivos

| Camada | Arquivo |
|--------|---------|
| Tela | `frontend/app/(tabs)/categorias.tsx` |
| API client | `frontend/src/api/services.ts` |
| Rotas | `museu_galeria/urls.py` + `apps/categorias/urls.py` |
| Lógica | `apps/categorias/views.py` |
| JSON | `apps/categorias/serializers.py` |
| Banco | `apps/categorias/models.py` → tabela `museu_categoriaobra` |

---

# Frontend — `categorias.tsx`

## Estado

```tsx
const { canStaff } = useAuth();
```
Funcionário ou admin? Se não → tela bloqueada.

```tsx
const [items, setItems] = useState<CategoriaObra[]>([]);
```
Lista de categorias da API.

```tsx
const [loading, setLoading] = useState(true);
```
Primeira carga → mostra loading.

```tsx
const [showForm, setShowForm] = useState(false);
```
Modal aberto ou fechado.

```tsx
const [editing, setEditing] = useState<CategoriaObra | null>(null);
```
`null` = criar | objeto = editar.

```tsx
const [nome, setNome] = useState('');
const [descricao, setDescricao] = useState('');
```
Campos do formulário.

---

## 1. Listar (abrir tela)

```tsx
const load = useCallback(async () => {
  setError(null);
  setItems(await fetchCategorias());
}, []);
```
Chama API e guarda em `items`.

```tsx
useEffect(() => {
  load().catch(...).finally(() => setLoading(false));
}, [load]);
```
Roda ao abrir a tela.

**→ Backend:** `GET /api/categorias-obra/`

---

## 2. Abrir formulário

```tsx
function abrirForm(cat?: CategoriaObra) {
  setEditing(cat ?? null);
  setNome(cat?.nome ?? '');
  setDescricao(cat?.descricao ?? '');
  setShowForm(true);
}
```

| Chamada | Resultado |
|---------|-----------|
| `abrirForm()` | Modal vazio → **criar** |
| `abrirForm(item)` | Modal preenchido → **editar** |

Ainda **não** chama o backend.

---

## 3. Salvar (criar ou editar)

```tsx
async function salvar() {
  if (!nome.trim()) {
    Alert.alert('Campo obrigatorio', 'Informe o nome.');
    return;
  }
  try {
    setSaving(true);
    if (editing) {
      await updateCategoria(editing.id, { nome: nome.trim(), descricao });
    } else {
      await createCategoria({ nome: nome.trim(), descricao });
    }
    setShowForm(false);
    await load();
    Alert.alert('Sucesso', editing ? 'Categoria atualizada.' : 'Categoria criada.');
  } catch (e) {
    Alert.alert('Erro', ...);
  } finally {
    setSaving(false);
  }
}
```

| `editing` | Função | Backend |
|-----------|--------|---------|
| objeto | `updateCategoria(id, {...})` | **PATCH** `/api/categorias-obra/{id}/` |
| `null` | `createCategoria({...})` | **POST** `/api/categorias-obra/` |

Depois: fecha modal → `load()` lista de novo.

---

## 4. Excluir

```tsx
function confirmarExclusao(cat: CategoriaObra) {
  Alert.alert('Excluir categoria', `Remover "${cat.nome}"?`, [
    { text: 'Cancelar', style: 'cancel' },
    {
      text: 'Excluir',
      style: 'destructive',
      onPress: async () => {
        await deleteCategoria(cat.id);
        await load();
      },
    },
  ]);
}
```

**→ Backend:** `DELETE /api/categorias-obra/{id}/`  
Se categoria tiver obras vinculadas, o banco **bloqueia** (FK `PROTECT`).

---

## Botões na UI

```tsx
if (!canStaff) return <ErrorState message="Acesso restrito a funcionarios." />;
```

```tsx
<Button label="+ Nova categoria" onPress={() => abrirForm()} />
<Button label="Editar" onPress={() => abrirForm(item)} />
<Button label="Excluir" onPress={() => confirmarExclusao(item)} />
<Button label="Salvar" onPress={salvar} />
```

Aba só aparece para staff em `(tabs)/_layout.tsx`:

```tsx
href: canStaff ? undefined : null
```

---

## `services.ts` — ponte com o backend

```ts
export const fetchCategorias = () =>
  apiGet('/categorias-obra/').then((d) => d.results);

export const createCategoria = (payload) =>
  apiPost('/categorias-obra/', payload);

export const updateCategoria = (id, payload) =>
  apiPatch(`/categorias-obra/${id}/`, payload);

export const deleteCategoria = (id) =>
  apiDelete(`/categorias-obra/${id}/`);
```

| Função | HTTP | Body |
|--------|------|------|
| `fetchCategorias` | GET | — |
| `createCategoria` | POST | `{ nome, descricao }` |
| `updateCategoria` | PATCH | `{ nome, descricao }` |
| `deleteCategoria` | DELETE | — |

---

# Backend

## `museu_galeria/urls.py`

```python
path('api/categorias-obra/', include('categorias.urls')),
```

Encaminha tudo que começa com `/api/categorias-obra/` para o app categorias.

---

## `apps/categorias/urls.py`

```python
router = SimpleRouter()
router.register('', views.CategoriaObraViewSet, basename='categorias-obra')

urlpatterns = [
    path('', include(router.urls)),
]
```

O **router** liga HTTP → ViewSet automaticamente:

| URL | HTTP | Método DRF |
|-----|------|------------|
| `/api/categorias-obra/` | GET | `list()` |
| `/api/categorias-obra/` | POST | `create()` |
| `/api/categorias-obra/{id}/` | PATCH | `partial_update()` |
| `/api/categorias-obra/{id}/` | DELETE | `destroy()` |

---

## `apps/categorias/views.py`

```python
class CategoriaObraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaObra.objects.all()
    serializer_class = CategoriaObraSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
```

| Linha | O que faz |
|-------|-----------|
| `ModelViewSet` | CRUD pronto — você **não escreve** `list()`, `create()`, etc. |
| `queryset` | Busca padrão: todas as categorias |
| `serializer_class` | Quem converte JSON ↔ Python |
| `search_fields` | Permite `?search=pintura` na URL |
| `ordering_fields` | Permite `?ordering=nome` na URL |

### O que roda por baixo (herdado do DRF)

**`list()` — GET (abrir tela)**
1. `CategoriaObra.objects.all()` → SELECT
2. Paginação (20 por página)
3. Serializer → JSON
4. Resposta `{ count, results: [...] }`

**`create()` — POST (adicionar)**
1. Serializer valida `{ nome, descricao }`
2. `serializer.save()` → INSERT
3. Resposta **201** com `{ id, nome, descricao }`

**`partial_update()` — PATCH (editar)**
1. Busca categoria pelo `id` na URL
2. Valida campos enviados
3. `save()` → UPDATE
4. Resposta **200**

**`destroy()` — DELETE (excluir)**
1. Busca categoria pelo `id`
2. `delete()` → DELETE SQL
3. Resposta **204**

---

## `apps/categorias/serializers.py`

```python
class CategoriaObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaObra
        fields = '__all__'
```

| Parte | Função |
|-------|--------|
| `model` | Liga ao model Django |
| `fields = '__all__'` | JSON com `id`, `nome`, `descricao` |

- **Leitura (GET):** model → JSON  
- **Escrita (POST/PATCH):** JSON → valida → grava  

---

## `apps/categorias/models.py`

```python
class CategoriaObra(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        db_table = 'museu_categoriaobra'
```

| Campo | Banco |
|-------|-------|
| `nome` | Obrigatório, até 100 caracteres |
| `descricao` | Opcional |
| `db_table` | Tabela `museu_categoriaobra` (Oracle/SQLite) |

Obras usam FK: `ObraArte.categoria` → `on_delete=PROTECT` (não exclui categoria com obras).

---

# Fluxos completos

## Abrir tela

```
load()
  → fetchCategorias()
  → GET /api/categorias-obra/
  → list() → SELECT → JSON
  → setItems() → FlatList
```

## Adicionar

```
"+ Nova categoria" → abrirForm()
  → preenche → Salvar → salvar()
  → createCategoria({ nome, descricao })
  → POST /api/categorias-obra/
  → create() → INSERT
  → load() → lista atualizada
```

## Editar

```
"Editar" → abrirForm(item) → Salvar → salvar()
  → updateCategoria(id, { nome, descricao })
  → PATCH /api/categorias-obra/{id}/
  → partial_update() → UPDATE
  → load()
```

## Excluir

```
"Excluir" → confirma → deleteCategoria(id)
  → DELETE /api/categorias-obra/{id}/
  → destroy() → DELETE SQL
  → load()
```

---

# Uso em Obras

```tsx
const cats = await fetchCategorias();
await createObra({ ..., categoria: categoriaId });
```

Mesmo GET de categorias alimenta o picker ao cadastrar obra.

---

# Apresentação (1 frase)

> A tela guarda estado e chama `services.ts`; o Django recebe na **ViewSet**, o **serializer** valida e o **model** grava em `museu_categoriaobra`. GET/POST/PATCH/DELETE vêm do **ModelViewSet** — não precisam ser escritos na view.

---

# Testar

```bash
# Backend
cd A3 && .venv/bin/python manage.py runserver 0.0.0.0:8001

# App
cd frontend && npm start

# API no navegador (HTML do DRF)
open http://127.0.0.1:8001/api/categorias-obra/

# curl
curl http://127.0.0.1:8001/api/categorias-obra/
curl -X POST http://127.0.0.1:8001/api/categorias-obra/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","descricao":"Demo"}'
```
