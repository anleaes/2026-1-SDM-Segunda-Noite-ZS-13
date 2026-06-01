# Estratégia de branches

| Branch | Uso |
|--------|-----|
| `main` | Versão estável (releases) |
| `develop` | Integração contínua do time |
| `feature/*` | Uma branch por entrega / módulo |

## Branches de feature

| Branch | Conteúdo |
|--------|----------|
| `feature/models-uml` | Models Django a partir do diagrama UML |
| `feature/api-rest` | Serializers, views e rotas REST |
| `feature/admin-oracle` | Django Admin e conexão Oracle |
| `feature/gestao-acervo` | Seed demo e gestão do acervo |
| `feature/artista-obra` | Vínculo artista ↔ obra |
| `feature/exposicao-obra` | App exposições (N:N) |
| `feature/restauracao-obras` | Restauração e certificados |
| `feature/usabilidade` | Filtros, paginação e UX da API |

## Fluxo

1. Atualizar `develop`: `git pull origin develop`
2. Criar ou usar `feature/nome`: `git switch feature/nome`
3. Commits pequenos e descritivos na feature
4. Abrir Pull Request para `develop`
5. Após validação, merge em `develop` e depois release em `main`
