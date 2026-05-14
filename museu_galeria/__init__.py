# Django 4.2 usa o driver cx_Oracle por padrão; oracledb é o substituto moderno.
try:
    import oracledb
    import sys

    oracledb.version = '8.3.0'
    sys.modules['cx_Oracle'] = oracledb
except ImportError:
    pass
