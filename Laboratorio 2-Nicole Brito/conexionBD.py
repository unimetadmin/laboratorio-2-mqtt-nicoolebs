		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# CONEXIÓN DE LA BASE DE DATOS

#Importaciones
import psycopg2

#Conexión con la Base de datos
def get_connection():
    connection = psycopg2.connect(
        user = "vtkzhkkf",
        password = "w8yb7qjFvIohzaCOyH7oAenyA8_R2gXN",
        host = "queenie.db.elephantsql.com",
        port = "5432",
        database = "vtkzhkkf"
    )
    return connection

def close_connection(connection):
    if connection:
        connection.close()