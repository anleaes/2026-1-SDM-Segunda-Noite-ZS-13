# Museu Galeria — Frontend Vue.js

Frontend web em **Vue 3 + Vite** conectado à API Django.

## Bibliotecas

| Lib | Uso |
|-----|-----|
| **Vue 3** | Framework |
| **Vite** | Build e dev server |
| **Vue Router** | Navegação |
| **Pinia** | Estado (login/sessão) |
| **Axios** | Chamadas HTTP à API |
| **Element Plus** | UI (tabelas, forms, cards, tags) |

## Telas

- Login (visitante / funcionário / artista)
- Início (dashboard)
- Galerias + detalhe
- Obras + detalhe + certificado
- Exposições + detalhe (comprar ingresso, reservar, avaliar)
- Perfil

## Como rodar

### 1. Backend (raiz do projeto)

```bash
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend Vue

```bash
cd frontend-vue
npm install
npm run dev
```

Abra: **http://localhost:5173**

> O Vite faz **proxy** de `/api` → `http://127.0.0.1:8000` (sem problema de CORS no dev).

## Usuários demo

| Login | Perfil |
|-------|--------|
| `nathan.visitante` | Visitante |
| `nathan.funcionario` | Funcionário |
| `nathan.artista` | Artista |

Rode `python manage.py seed_demo` se os usuários não existirem.

## Estrutura

```
frontend-vue/
├── src/
│   ├── api/          # Axios + serviços
│   ├── stores/       # Pinia (auth)
│   ├── router/       # Rotas
│   ├── layouts/      # Layout com menu
│   └── views/        # Telas
├── vite.config.js    # Proxy para Django
└── package.json
```
