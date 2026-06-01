# Museu & Galeria — Backend (SDM 2026.1)

API REST em **Django** para gestão de museu e galeria: acervo (obras, artistas, certificados, restauração), exposições, visitação (ingressos, reservas, pagamentos) e autenticação de usuários.

Repositório da turma **Segunda Noite ZS-13** — disciplina de Sistemas de Informação.

## Requisitos

- Python 3.10+
- pip
- Oracle Database (opcional; ver [ORACLE.md](ORACLE.md)) ou SQLite para testes locais

## Instalação rápida

Passo a passo completo em [docs/SETUP.md](docs/SETUP.md).

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

## Diagrama

Modelo de dados: [diagrama.puml](diagrama.puml)

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| [docs/SETUP.md](docs/SETUP.md) | Instalação e comandos |
| [docs/API.md](docs/API.md) | Rotas da API REST |
| [ORACLE.md](ORACLE.md) | Configuração Oracle |
| [BRANCHES.md](BRANCHES.md) | Branches do Git |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Commits e PRs |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |
