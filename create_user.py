from database import get_connection
from hashing import hash_password
import pyodbc


username = "marco250"
password = "SZGXAz-250"

password_hash = hash_password(password)

conexion = pyodbc.connect(
  "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.2.210,1433;"
        "DATABASE=Chinook;"
        "UID=sa;"
        "PWD=Marquitos2025;"
        "TrustServerCertificate=yes;"
)
cursor = conexion.cursor()

cursor.execute("""
    INSERT INTO dbo.Usuario (Username, PasswordHash, Activo)
    VALUES (?, ?, 1)
""", username, password_hash)

conexion.commit()
conexion.close()

print("Usuario creado correctamente")