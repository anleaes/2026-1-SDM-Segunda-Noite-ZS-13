"""
Teste de conexão Oracle Cloud ADB — template oficial Oracle.
Uso: python oracle_connect_test.py
"""
import os
from pathlib import Path

import oracledb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

DB_USER = os.getenv('ORACLE_USER', 'admin')
DB_PASSWORD = os.getenv('ORACLE_PASSWORD', '')
WALLET_DIR = str(Path(__file__).resolve().parent / os.getenv('ORACLE_WALLET_DIR', 'wallet'))
TNS_ALIAS = os.getenv('ORACLE_NAME', 'gerenciamentodemuseu1_high')

# String TCPS gerada pelo console Oracle (Database connection)
CONNECT_STRING = (
    '(description=(retry_count=20)(retry_delay=3)'
    '(address=(protocol=tcps)(port=1522)(host=adb.sa-saopaulo-1.oraclecloud.com))'
    '(connect_data=(service_name=gbe06e8c506932e_gerenciamentodemuseu1_high.adb.oraclecloud.com))'
    '(security=(ssl_server_dn_match=yes)))'
)


def run_app():
    try:
        pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=TNS_ALIAS,
            config_dir=WALLET_DIR,
            min=1,
            max=2,
        )
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1 FROM DUAL')
                result = cursor.fetchone()
                if result:
                    print(f'Conectado! Resultado: {result[0]}')
                    cursor.execute('SELECT USER FROM DUAL')
                    print(f'Usuário: {cursor.fetchone()[0]}')
    except oracledb.Error as e:
        print(f'Erro ao conectar: {e}')
    except Exception:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_app()
