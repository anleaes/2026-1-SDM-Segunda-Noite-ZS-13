# Setup do ambiente

## 1. Clonar e entrar na pasta

```bash
git clone https://github.com/anleaes/2026-1-SDM-Segunda-Noite-ZS-13.git
cd 2026-1-SDM-Segunda-Noite-ZS-13
git switch develop
```

## 2. Ambiente virtual Python

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env`: `SECRET_KEY`, `DB_ENGINE` (`sqlite` ou `oracle`) e credenciais Oracle se aplicável.

## 4. Banco e dados iniciais

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
```

## 5. Servidor

```bash
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/
