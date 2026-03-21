import pyodbc


def get_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=192.168.2.210,1433;"
        "DATABASE=Chinook;"
        "UID=sa;"
        "PWD=Marquitos2025;"
        "TrustServerCertificate=yes;"
    )
    return connection