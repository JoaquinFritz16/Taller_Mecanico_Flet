import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='root', 
            database='Taller_Mecanico',
            ssl_disabled=True
        )
        if connection.is_connected():
            print("Conexión a la base de datos exitosa.")
            return connection
    except Exception as ex:
        print(f"Error al conectar con la base de datos: {ex}")
        return None