# Museu Galeria — App Mobile (React Native)

App mobile em **React Native + Expo** conectado à API Django do projeto.

## Stack

- Expo SDK 52
- Expo Router (navegação por arquivos)
- TypeScript
- API REST Django (`/api/`)

## Telas

| Tela | Funcionalidade |
|------|----------------|
| **Login** | Entrada por perfil (visitante, funcionário, artista) |
| **Início** | Dashboard com totais |
| **Galerias** | Lista e detalhe |
| **Obras** | Lista, detalhe e certificado |
| **Exposições** | Lista, detalhe, obras vinculadas |
| **Perfil** | Dados do usuário, ingressos, reservas, avaliações |

### Ações do visitante (na exposição)

- Comprar ingresso
- Fazer reserva
- Enviar avaliação

## Usuários demo

| Login | Perfil | Senha* |
|-------|--------|--------|
| `nathan.visitante` | Visitante | *(login sem senha na API)* |
| `nathan.funcionario` | Funcionário | — |
| `nathan.artista` | Artista | — |

\* O app identifica o usuário pela API (projeto acadêmico, API aberta).

## Como rodar

### 1. Backend (pasta raiz do projeto)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

> Use `0.0.0.0:8000` para o celular físico acessar na rede Wi‑Fi.

### 2. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npx expo start
```

### 3. URL da API

Edite `frontend/.env`:

| Ambiente | EXPO_PUBLIC_API_URL |
|----------|---------------------|
| Simulador iOS | `http://127.0.0.1:8000/api` |
| Emulador Android | `http://10.0.2.2:8000/api` |
| Celular físico | `http://SEU_IP_LOCAL:8000/api` |

Descubra seu IP no Mac: `ipconfig getifaddr en0`

## Estrutura

```
frontend/
├── app/                 # Rotas (Expo Router)
│   ├── (tabs)/          # Abas principais
│   ├── galeria/[id].tsx
│   ├── obra/[id].tsx
│   └── exposicao/[id].tsx
└── src/
    ├── api/             # Cliente HTTP e serviços
    ├── components/      # UI reutilizável
    ├── context/         # AuthContext
    └── theme/           # Cores e espaçamento
```

## Atalhos Expo

- `i` — abrir simulador iOS
- `a` — abrir emulador Android
- `w` — abrir no navegador
