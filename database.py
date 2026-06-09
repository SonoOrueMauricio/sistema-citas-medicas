import psycopg2


def conectar():
    conexion = psycopg2.connect(
        host="localhost",
        dbname="proyecto_curso_integrador",
        user="postgres",
        password="123"
    )

    conexion.set_client_encoding('LATIN1')

    return conexion
