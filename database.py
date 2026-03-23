import pyodbc
from settings import settings

def get_connection():
    connection_string = (
        f"DRIVER={{{settings.DB_DRIVER}}};"
        f"SERVER={settings.DB_SERVER};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD};"
        f"TrustServerCertificate={settings.DB_TRUST_CERT};"
    )
    return pyodbc.connect(connection_string)