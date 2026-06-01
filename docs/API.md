# Referência rápida da API

Base URL local: `http://127.0.0.1:8000`

| Prefixo | Recursos |
|---------|----------|
| `/api/health/` | Status da API e conexão com o banco (`GET`) |
| `/api/auth/` | Login e tokens |
| `/api/usuarios/` | Usuários |
| `/api/funcionarios/` | Funcionários |
| `/api/visitantes/` | Visitantes |
| `/api/artistas/` | Artistas |
| `/api/galerias/` | Galerias |
| `/api/categorias-obra/` | Categorias de obra |
| `/api/obras/` | Obras |
| `/api/certificados/` | Certificados |
| `/api/artista-obras/` | Vínculo artista–obra |
| `/api/restauracoes/` | Restaurações |
| `/api/exposicoes/` | Exposições |
| `/api/exposicao-obras/` | Obras em exposição |
| `/api/ingressos/` | Ingressos |
| `/api/reservas/` | Reservas |
| `/api/avaliacoes/` | Avaliações |
| `/api/pagamentos/` | Pagamentos |
| `/admin/` | Django Admin |

Autenticação e filtros seguem as views em `apps/` e `museu/`.
