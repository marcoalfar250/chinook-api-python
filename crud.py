from database import get_connection


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

