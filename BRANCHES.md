# Estratégia de branches

| Branch | Uso |
|--------|-----|
| `main` | Versão estável (releases) |
| `develop` | Integração contínua do time |
| `feature/*` | Uma branch por entrega / módulo |

## Branches de feature — entregas iniciais

| Branch | Conteúdo |
|--------|----------|
| `feature/models-uml` | Models Django a partir do diagrama UML |
| `feature/api-rest` | Serializers, views e rotas REST |
| `feature/admin-oracle` | Django Admin e conexão Oracle |
| `feature/gestao-acervo` | Seed demo e gestão do acervo |
| `feature/artista-obra` | Vínculo artista ↔ obra |
| `feature/crud-artistas` | CRUD e gestão de artistas |
| `feature/exposicao-obra` | App exposições (N:N) |
| `feature/restauracao-obras` | Restauração de obras |
| `feature/usabilidade` | Filtros, paginação e UX da API |

## Branches de feature — módulos e evolução

Criadas a partir de `develop` para dividir trabalho por área (mesma base de código até o primeiro commit em cada branch).

| Branch | Conteúdo |
|--------|----------|
| `feature/galerias` | App galerias (locais físicos) |
| `feature/categorias` | Categorias de obra |
| `feature/contas-autenticacao` | Login, cadastro, usuários e papéis |
| `feature/certificados` | Certificados de autenticidade |
| `feature/visitacao-ingressos` | Ingressos |
| `feature/visitacao-reservas` | Reservas |
| `feature/integracao-frontend` | Integração com frontend Vue (CORS, URLs) |
| `feature/testes-api` | Testes automatizados da API |
| `feature/relatorios-acervo` | Relatórios do acervo |
| `feature/documentacao` | README, setup, API e docs do repositório |

## Fluxo

1. Atualizar `develop`: `git pull origin develop`
2. Criar ou usar `feature/nome`: `git switch feature/nome`
3. Commits pequenos e descritivos na feature
4. Abrir Pull Request para `develop`
5. Após validação, merge em `develop` e depois release em `main`

## Comandos úteis

```bash
# Listar branches locais e remotas
git branch -a

# Criar branch local a partir de develop (se ainda não existir no PC)
git fetch origin
git switch -c feature/nome origin/feature/nome

# Publicar commits da feature
git push origin feature/nome
```
