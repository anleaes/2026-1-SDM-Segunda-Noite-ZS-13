# Usando Oracle Database no projeto

Guia do que você precisa instalar e configurar para o Django conectar no Oracle.

---

## Resumo rápido

| Item | Obrigatório? | Para quê |
|------|--------------|----------|
| **Oracle Database** | Sim | O banco em si (XE, da faculdade ou nuvem) |
| **Python `oracledb`** | Sim | Driver que conecta Django ↔ Oracle |
| **Oracle Instant Client** | Não* | Só se usar Oracle antigo ou modo Thick |
| **Usuário/schema no Oracle** | Sim | Onde as tabelas serão criadas |
| **Arquivo `.env`** | Sim | Credenciais sem colocar senha no código |

\* O `oracledb` em **modo Thin** (padrão) conecta direto, sem instalar Oracle Client. Funciona com Oracle **12.1+**. O Django 4.2 exige oficialmente Oracle **19c+**.

---

## 1. Banco Oracle

Você precisa de **uma instância Oracle rodando**. Opções comuns:

### Opção A — Oracle XE (grátis, local)

1. Baixe: https://www.oracle.com/database/technologies/xe-downloads.html  
2. Instale e anote:
   - **Host:** `localhost`
   - **Porta:** `1521`
   - **Service name:** geralmente `XEPDB1` (Pluggable Database)

### Opção B — Oracle da faculdade

Peça ao professor ou TI:
- Host (IP ou hostname)
- Porta (geralmente `1521`)
- Service name ou SID
- Usuário e senha
- Se precisa VPN para acessar

### Opção C — Oracle Cloud (Free Tier)

1. Crie conta em https://cloud.oracle.com  
2. Crie um **Autonomous Database** (Always Free)  
3. Baixe a **wallet** (arquivo ZIP com credenciais)
4. Use o connection string que a Oracle fornece

---

## 2. Dependências Python

No projeto:

```bash
pip3 install -r requirements.txt
```

Isso instala o pacote **`oracledb`**, que substitui o antigo `cx_Oracle`.

O arquivo `museu_galeria/__init__.py` já faz o mapeamento para o Django 4.2 reconhecer o driver.

---

## 3. Criar usuário no Oracle

Antes do `migrate`, crie um usuário/schema para o projeto. Exemplo no **SQL*Plus** ou **SQL Developer**:

```sql
-- Conecte como SYS ou admin
CREATE USER museu IDENTIFIED BY sua_senha_aqui;

GRANT CONNECT, RESOURCE TO museu;
GRANT CREATE VIEW TO museu;
GRANT UNLIMITED TABLESPACE TO museu;
```

> **Na faculdade:** muitas vezes o professor já entrega o usuário pronto.

---

## 4. Configurar o `.env`

```bash
cp .env.example .env
```

Edite o `.env`:

```env
DB_ENGINE=oracle
ORACLE_NAME=localhost:1521/XEPDB1
ORACLE_USER=museu
ORACLE_PASSWORD=sua_senha_aqui
```

### Formato do `ORACLE_NAME`

Use **Easy Connect** (mais simples, sem `tnsnames.ora`):

```
host:porta/nome_do_servico
```

| Cenário | Exemplo |
|---------|---------|
| Oracle XE local | `localhost:1521/XEPDB1` |
| Servidor remoto | `10.0.0.5:1521/ORCLPDB1` |
| Faculdade | o que o TI informar |

**Importante:** sempre informe a **porta** (1521). Se deixar vazio, pode dar erro `DPY-4027`.

---

## 5. Rodar migrações

```bash
python3 manage.py migrate
```

Isso cria todas as tabelas do diagrama UML no Oracle.

Para conferir:

```bash
python3 manage.py dbshell
```

No SQL*Plus/SQL Developer, as tabelas aparecem com prefixo do app, ex.: `MUSEU_GALERIA`, `MUSEU_USUARIO`, etc.

---

## 6. Testar conexão

```bash
python3 manage.py check
python3 manage.py runserver
```

Se conectar, acesse http://127.0.0.1:8000/api/galerias/

---

## O que mudou no código

| Arquivo | Mudança |
|---------|---------|
| `requirements.txt` | Adicionado `oracledb` e `python-dotenv` |
| `museu_galeria/__init__.py` | Compatibilidade Django 4.2 + oracledb |
| `museu_galeria/settings.py` | Lê `.env` e escolhe SQLite ou Oracle |
| `.env.example` | Modelo de configuração |

**Sem `.env` ou com `DB_ENGINE=sqlite`:** continua usando SQLite (como antes).

---

## Erros comuns

### `ModuleNotFoundError: No module named 'oracledb'`

```bash
pip3 install oracledb
```

### `Oracle 19 or later is required (found 12.x)`

O Django 4.2 exige Oracle 19c+. Soluções:
- Usar Oracle 19c ou superior (XE 21c, por exemplo)
- Pedir ao professor um banco compatível
- *(Último recurso acadêmico)* usar SQLite para desenvolvimento

### `DPY-6001: Cannot connect to database`

- Oracle está rodando?
- Host, porta e service name corretos no `.env`?
- Firewall bloqueando a porta 1521?
- Usuário/senha corretos?

### `ORA-01017: invalid username/password`

Usuário ou senha errados no `.env`.

### `ORA-01950: no privileges on tablespace`

Falta permissão. Rode:

```sql
GRANT UNLIMITED TABLESPACE TO museu;
```

---

## O que falar na apresentação

> "Configurei o backend para suportar Oracle Database. O Django usa o driver oracledb para conectar via string host:porta/serviço. As credenciais ficam no arquivo .env por segurança. O mesmo código de models e API funciona tanto com SQLite quanto com Oracle — só muda a configuração do banco."

---

## Checklist

- [ ] Oracle instalado ou acesso ao servidor da faculdade
- [ ] Usuário `museu` (ou equivalente) criado com permissões
- [ ] `pip3 install -r requirements.txt`
- [ ] Arquivo `.env` criado a partir de `.env.example`
- [ ] `python3 manage.py migrate` executado com sucesso
- [ ] API respondendo em `/api/galerias/`
