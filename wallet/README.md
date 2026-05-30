# Wallet Oracle Cloud (Autonomous Database)

O Oracle Autonomous Database **exige** o wallet para conectar.

## Como baixar

1. Acesse https://cloud.oracle.com
2. **Oracle Database** → **Autonomous Database**
3. Abra **Gerenciamentodemuseu1**
4. Clique em **DB Connection**
5. **Download Wallet**
6. Defina uma senha do wallet (anote — pode ser a mesma do admin)
7. Extraia **todos** os arquivos desta pasta `wallet/`:

```
wallet/
├── cwallet.sso
├── ewallet.p12
├── keystore.jks
├── ojdbc.properties
├── sqlnet.ora
├── tnsnames.ora
└── truststore.jks
```

8. Abra `tnsnames.ora` e confirme o alias (geralmente `gerenciamentodemuseu1_high`)

## Depois de extrair

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```
