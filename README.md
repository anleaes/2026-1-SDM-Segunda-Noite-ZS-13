# Sistema de Gerenciamento de Museus e Galerias de Arte

Backend **Django REST** + app mobile **React Native (Expo)** + banco **Oracle Autonomous Database**.

Repositórios:
- **Backend:** https://github.com/anleaes/2026-1-SDM-Segunda-Noite-ZS-13
- **App mobile:** https://github.com/anleaes/2026-1-SDM-Segunda-Noite-ZS-13-RN

---

## Visão geral da arquitetura

```
┌─────────────────┐     HTTP/JSON      ┌──────────────────────────────────┐
│  App React      │  POST/GET/PATCH    │  Django (A3/)                    │
│  Native (Expo)  │ ─────────────────► │  museu_galeria/  → configuração  │
│  frontend/      │                    │  apps/           → regras/API    │
└─────────────────┘                    └──────────────┬───────────────────┘
                                                      │
                                                      ▼
                                           ┌──────────────────────┐
                                           │  Oracle Cloud (ADB)  │
                                           │  tabelas MUSEU_*     │
                                           └──────────────────────┘

┌─────────────────┐
│  Django Admin   │  /admin/  →  grava direto no banco (sem app mobile)
└─────────────────┘
```

O app **não fala com o Oracle**. Ele chama a **API REST** (`/api/...`). Quem grava no banco é sempre o **Django**, via **models**.

---

## Estrutura de pastas

```
A3/
├── manage.py                 # Comando principal: runserver, migrate, seed_demo
├── .env                      # Credenciais (Oracle, SECRET_KEY) — não commitar
├── wallet/                   # Wallet SSL do Oracle Cloud (obrigatório para ADB)
├── museu_galeria/            # Projeto Django (configuração global)
├── apps/                     # Apps de negócio (galerias, obras, etc.)
│   ├── contas/               # Usuários, login, perfis
│   ├── galerias/
│   ├── categorias/
│   ├── obras/
│   ├── exposicoes/
│   └── visitacao/            # Ingressos, reservas, pagamentos, avaliações
├── frontend/                 # App React Native (Expo)
├── diagrama.puml             # Diagrama UML do sistema
└── ORACLE.md                 # Guia de conexão Oracle
```

---

## O que é `museu_galeria/`?

É o **projeto Django** — a “casca” que configura tudo. **Não é um app de negócio** (não tem Galeria, Obra, etc.). Só liga as peças.

| Arquivo | Função |
|---------|--------|
| **`settings.py`** | Configuração central: apps instalados, banco Oracle/SQLite, CORS, REST Framework, idioma `pt-br`, usuário customizado (`contas.Usuario`) |
| **`urls.py`** | Rotas principais: `/admin/`, `/api/galerias/`, `/api/obras/`, etc. |
| **`wsgi.py`** | Ponto de entrada para servidores de produção (Gunicorn, etc.) |
| **`asgi.py`** | Entrada para async/WebSockets (não usado ativamente no projeto) |
| **`__init__.py`** | Compatibilidade **oracledb** ↔ Django Oracle backend |

### Detalhes importantes do `settings.py`

```python
APPS_DIR = .../apps
sys.path.insert(0, APPS_DIR)   # permite importar "contas", "galerias" sem "apps."
```

```python
INSTALLED_APPS = [
    'contas', 'galerias', 'categorias', 'obras', 'exposicoes', 'visitacao',
    ...
]
```

```python
DB_ENGINE=oracle  # no .env → usa Oracle + wallet
AUTH_USER_MODEL = 'contas.Usuario'  # usuário customizado (visitante, funcionário, artista)
```

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['AllowAny'],  # API aberta (sem token JWT hoje)
    'PAGE_SIZE': 20,  # paginação automática
}
```

---

## O que tem em cada `apps/<nome>/`?

Cada app segue o **mesmo padrão**. Exemplo: `apps/galerias/`

| Arquivo | Grava no banco? | O que faz |
|---------|-----------------|-----------|
| **`models.py`** | **Sim** (`.save()`, `.objects.create()`) | Define tabelas e colunas. **Coração do banco.** |
| **`serializers.py`** | Indiretamente (`serializer.save()`) | Converte JSON ↔ Python. Valida dados da API. |
| **`views.py`** | Indiretamente | Recebe HTTP (GET/POST/PATCH/DELETE). `ModelViewSet` = CRUD automático. |
| **`urls.py`** | Não | Mapeia URL → view (`/api/galerias/` → `GaleriaViewSet`) |
| **`admin.py`** | Indiretamente | Painel web `/admin/` para criar/editar registros |
| **`filters.py`** | **Não** | Só filtra consultas (`?categoria=1`, `?search=MASP`) |
| **`apps.py`** | Não | Registra o app no Django (`GaleriasConfig`) |
| **`migrations/`** | Cria estrutura | Scripts que criam/alteram tabelas (`migrate`) |
| **`tests.py`** | Não | Testes automatizados (stubs vazios hoje) |

### Apps e entidades

| App | Models principais | Tabela Oracle (exemplo) |
|-----|-------------------|-------------------------|
| **contas** | Usuario, Funcionario, Visitante, Artista | `MUSEU_USUARIO`, `MUSEU_FUNCIONARIO`, ... |
| **galerias** | Galeria | `MUSEU_GALERIA` |
| **categorias** | CategoriaObra | `MUSEU_CATEGORIAOBRA` |
| **obras** | ObraArte, Certificado, ArtistaObra, Restauracao | `MUSEU_OBRAARTE`, ... |
| **exposicoes** | Exposicao, ExposicaoObra | `MUSEU_EXPOSICAO`, `MUSEU_EXPOSICAOOBRA` |
| **visitacao** | Ingresso, Reserva, Avaliacao, Pagamento | `MUSEU_INGRESSO`, ... |

---

## `class Meta` — models vs serializers

Aparece nos **dois**, mas com **funções diferentes**:

### No `models.py` (Django ORM → banco)

```python
class Galeria(models.Model):
    nome = models.CharField(max_length=200)
    ...

    class Meta:
        db_table = 'museu_galeria'      # nome da tabela no Oracle
        verbose_name = 'Galeria'        # label no Admin
        verbose_name_plural = 'Galerias'
```

### No `serializers.py` (DRF → API JSON)

```python
class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeria           # qual model representa
        fields = '__all__'        # campos que vão no JSON
```

| | Meta do **Model** | Meta do **Serializer** |
|--|-------------------|------------------------|
| Configura | Tabela, Admin | JSON da API |
| Grava no banco? | Define onde grava | Não — só valida e repassa |

---

## Como os dados entram no banco (fluxo completo)

### Via API (app mobile ou Postman)

```
1. App chama:  POST /api/galerias/  {"nome": "MASP", "endereco": "...", "aberta": true}

2. urls.py     → encaminha para GaleriaViewSet

3. views.py    → ModelViewSet.create() recebe o POST

4. serializers → valida JSON, chama serializer.save()

5. models.py   → Galeria.objects.create(...)  ou  instance.save()

6. Oracle      → INSERT INTO museu_galeria (...)
```

### Via Django Admin

```
/admin/ → formulário → Salvar → model.save() → Oracle
```

### Via seed (dados de demo)

```bash
python manage.py seed_demo
```

Grava direto com `objects.create()` em `apps/contas/management/commands/seed_demo.py`.

### Via métodos do model (UML)

```python
galeria.abrir_galeria()   # self.aberta = True; self.save()
visitante.comprar_ingresso(...)  # Ingresso.objects.create(...)
```

---

## Mapa da API REST

| Método | URL | Ação | Grava? |
|--------|-----|------|--------|
| GET | `/api/galerias/` | Listar | Não |
| POST | `/api/galerias/` | Criar | **Sim** |
| PATCH | `/api/galerias/{id}/` | Atualizar | **Sim** |
| DELETE | `/api/galerias/{id}/` | Excluir | **Sim** |
| POST | `/api/auth/login/` | Login | Não |
| POST | `/api/auth/register/` | Cadastro visitante | **Sim** |
| POST | `/api/ingressos/` | Comprar ingresso | **Sim** |
| POST | `/api/pagamentos/` | Registrar pagamento | **Sim** |

Lista completa em `museu_galeria/urls.py`.

---

## Perfis de usuário (diagrama UML)

| Perfil | O que faz no app | O que faz no Admin |
|--------|------------------|-------------------|
| **Visitante** | Ingresso, reserva, avaliação | — |
| **Funcionário** | Galerias, obras, exposições, restauração | Pode usar Admin |
| **Artista** | Portfolio, vincular obras | — |
| **Admin** | Tudo + painel de usuários | Acesso total |

Usuários demo (`seed_demo`):

| Usuário | Senha | Perfil |
|---------|-------|--------|
| nathan.visitante | demo123 | Visitante |
| nathan.funcionario | demo123 | Funcionário |
| nathan.artista | demo123 | Artista |
| admin | admin123 | Administrador |

---

## Como rodar

### Backend

```bash
cd A3
conda activate museu-galeria
python manage.py runserver 0.0.0.0:8001
```

### App mobile

```bash
cd frontend
# .env → EXPO_PUBLIC_API_URL=http://SEU_IP:8001/api
npm start
```

### Banco

```bash
python manage.py migrate      # cria tabelas
python manage.py seed_demo      # popula dados de teste
```

Conexão Oracle e DBeaver: veja **ORACLE.md**.

---

## O que **não** grava no banco

- `filters.py` — só filtra leituras
- `urls.py` — só rotas
- `apps.py` — só configuração
- `frontend/src/api/client.ts` — só HTTP
- `frontend/src/api/types.ts` — só tipos TypeScript

---

## Diagrama UML

O arquivo `diagrama.puml` define classes, enums, relacionamentos e métodos (`abrirGaleria`, `comprarIngresso`, `gerarRelatorio`, etc.). A implementação está nos **models** (métodos) e na **API** (endpoints CRUD).

---

## Referência rápida para apresentação

> "O projeto Django usa a pasta **museu_galeria** só para configuração global. A lógica de negócio fica em **apps/**, cada uma com **models** (banco), **serializers** (JSON), **views** (API) e **admin** (painel web). O app React Native consome a API REST; o Oracle armazena as tabelas `MUSEU_*`. O `class Meta` no model configura a tabela; no serializer configura o JSON."
