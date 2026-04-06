from database import get_connection
import math

def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT CustomerId, FirstName, LastName, Country, Email
        FROM Customer
        ORDER BY CustomerId
    """)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "customer_id": row.CustomerId,
            "first_name": row.FirstName,
            "last_name": row.LastName,
            "country": row.Country,
            "email": row.Email
        })

    return resultado

def obtener_clientes_paginado(
        page: int = 1, 
        page_size: int = 10, 
        country: str = None, 
        nombre: str = None,
        sort_by: str = "CustomerId",
        sort_order: str = "asc"
        ):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size

    columnas_permitidas = {
        "CustomerId": "CustomerId",
        "FirstName": "FirstName",
        "LastName": "LastName",
        "Country": "Country",
        "Email": "Email"
        }
    
    if sort_by not in columnas_permitidas:
        sort_by = "CustomerId"

    if sort_order.lower() not in ["asc", "desc"]:
        sort_order = "asc"

    columna_orden = columnas_permitidas[sort_by]
    direccion_orden = sort_order.upper()

    where_sql = " WHERE 1 = 1 "
    params = []

    if country:
        where_sql += " AND Country = ?"
        params.append(country)

    if nombre:
        where_sql += " AND (FirstName LIKE ? OR LastName LIKE ?)"
        params.append(f"%{nombre}%")
        params.append(f"%{nombre}%")

    sql_total = f"""
        SELECT COUNT(*) AS Total
        FROM Customer
        {where_sql}
    """

    cursor.execute(sql_total, params)
    total = cursor.fetchone()[0]

    sql_data = f"""
        SELECT CustomerId, FirstName, LastName, Country, Email
        FROM Customer
        {where_sql}
        ORDER BY {columna_orden} {direccion_orden}
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """

    data_params = params.copy()
    data_params.extend([offset, page_size])

    cursor.execute(sql_data, data_params)
    rows = cursor.fetchall()

    conn.close()

    data = []
    for row in rows:
        data.append({
            "customer_id": row.CustomerId,
            "first_name": row.FirstName,
            "last_name": row.LastName,
            "country": row.Country,
            "email": row.Email
        })

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "sort_order": direccion_orden.lower(),
        "data": data
    }

def obtener_cliente_por_id(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT CustomerId, FirstName, LastName, Country, Email
        FROM Customer
        WHERE CustomerId = ?
    """, customer_id)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "customer_id": row.CustomerId,
        "first_name": row.FirstName,
        "last_name": row.LastName,
        "country": row.Country,
        "email": row.Email
    }

def obtener_artistas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ArtistId, Name
        FROM Artist
        ORDER BY Name
    """)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "artist_id": row.ArtistId,
            "name": row.Name
        })

    return resultado

def obtener_artitas_paginado(
        page: int = 1, 
        page_size: int = 10,
        nombre: str = None,
        sort_by: str = "ArtistId",
        sort_order: str = "asc"
):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size

    columnas_permitidas = {
        "ArtistId": "ArtistId",
        "Name": "Name"
        }
    
    if sort_by not in columnas_permitidas:
        sort_by = "ArtistId"

    if sort_order.lower() not in ["asc", "desc"]:
        sort_order = "asc"

    columna_orden = columnas_permitidas[sort_by]
    direccion_orden = sort_order.upper()

    where_sql = " WHERE 1 = 1 "
    params = []

    if nombre:
        where_sql += " AND Name LIKE ?"
        params.append(f"%{nombre}%")
    
    sql_total = f"""
        SELECT COUNT(*) AS Total
        FROM Artist
        {where_sql}
    """

    cursor.execute(sql_total, params)
    total = cursor.fetchone()[0]
    
    sql_data = f"""
        SELECT Name
        FROM Artist
        {where_sql}
        ORDER BY {columna_orden} {direccion_orden}
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """

    data_params = params.copy()
    data_params.extend([offset, page_size])

    cursor.execute(sql_data, data_params)
    rows = cursor.fetchall()

    conn.close()

    data = []
    for row in rows:
        data.append({
            "Name": row.Name          
        })

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "sort_order": direccion_orden.lower(),
        "data": data
    }

def obtener_albumes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.AlbumId,
            a.Title,
            ar.Name AS ArtistName
        FROM Album a
        INNER JOIN Artist ar
            ON a.ArtistId = ar.ArtistId
        ORDER BY a.AlbumId
    """)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "album_id": row.AlbumId,
            "title": row.Title,
            "artist_name": row.ArtistName
        })

    return resultado

def obtener_facturas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.InvoiceId,
            i.CustomerId,
            c.FirstName + ' ' + c.LastName AS CustomerName,
            CONVERT(VARCHAR, i.InvoiceDate, 120) AS InvoiceDate,
            i.Total
        FROM Invoice i
        INNER JOIN Customer c
            ON i.CustomerId = c.CustomerId
        ORDER BY i.InvoiceId
    """)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "invoice_id": row.InvoiceId,
            "customer_id": row.CustomerId,
            "customer_name": row.CustomerName,
            "invoice_date": row.InvoiceDate,
            "total": float(row.Total)
        })

    return resultado

def obtener_facturas_por_cliente(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.InvoiceId,
            i.CustomerId,
            c.FirstName + ' ' + c.LastName AS CustomerName,
            CONVERT(VARCHAR, i.InvoiceDate, 120) AS InvoiceDate,
            i.Total
        FROM Invoice i
        INNER JOIN Customer c
            ON i.CustomerId = c.CustomerId
        WHERE i.CustomerId = ?
        ORDER BY i.InvoiceId
    """, customer_id)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "invoice_id": row.InvoiceId,
            "customer_id": row.CustomerId,
            "customer_name": row.CustomerName,
            "invoice_date": row.InvoiceDate,
            "total": float(row.Total)
        })

    return resultado

def obtener_comentario():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, CustomerId, Comentario, CONVERT(VARCHAR, FechaRegistro, 120) AS FechaRegistro
        FROM dbo.ComentarioCliente
        ORDER BY Id
    """)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
         resultado.append({
            "id": row.Id,
            "customer_id": row.CustomerId,
            "comentario": row.Comentario,
            "fecha_registro": row.FechaRegistro
        })
    
    return resultado

def obtener_comentarios_por_cliente(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, CustomerId, Comentario, CONVERT(VARCHAR, FechaRegistro, 120) AS FechaRegistro
        FROM dbo.ComentarioCliente
        WHERE CustomerId = ?
        ORDER BY Id
    """, customer_id)

    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "id": row.Id,
            "customer_id": row.CustomerId,
            "comentario": row.Comentario,
            "fecha_registro": row.FechaRegistro
        })

    return resultado

def existe_cliente(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM Customer
        WHERE CustomerId = ?
    """, customer_id)

    row = cursor.fetchone()
    conn.close()

    return row is not None

def crear_comentario(customer_id: int, comentario: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dbo.ComentarioCliente (CustomerId, Comentario)
        OUTPUT INSERTED.Id, INSERTED.CustomerId, INSERTED.Comentario, CONVERT(VARCHAR, INSERTED.FechaRegistro, 120)
        VALUES (?, ?)
    """, customer_id, comentario)

    row = cursor.fetchone()
    conn.commit()
    conn.close()

    return {
        "id": row[0],
        "customer_id": row[1],
        "comentario": row[2],
        "fecha_registro": row[3]
    }

def obtener_usuario_por_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Username, PasswordHash, Activo
        FROM dbo.Usuario
        WHERE Username = ?
    """, username)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row.Id,
        "username": row.Username,
        "password_hash": row.PasswordHash,
        "activo": bool(row.Activo)
    }