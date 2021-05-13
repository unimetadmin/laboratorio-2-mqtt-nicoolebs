		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# PUBLICACIÓN DE LAS PERSONAS DE LA SALA


#Importaciones
import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime

#Importaciones para la BD

import psycopg2
import conexionBD
import json

#Def para obtener el ultimo tiempo que se necesita para insertar el siguiente dato
def ultima_fecha_personas():
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """SELECT fecha_personas FROM public.personas ORDER BY ID DESC LIMIT 1;"""
		cursor.execute(query)
		fecha = cursor.fetchone()
		conexionBD.close_connection(conexion)
		return fecha[0]

	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)


#Definición de on_connect para saber si estoy conectado
def on_connect(client, userdata, flags, rc):
	print('Conectado el publicador')

def main():

    #Cliente
	client = paho.mqtt.client.Client("Personas", False)
    #Calidad del Servicio
	client.qos = 0
    #Conexión
	client.connect(host='localhost')

    #Hora Base Personas
	horaPersonas = ultima_fecha_personas()

	while(True):

        #CANTIDAD PERSONAS:

        #Aumento de 1 minuto
		horaPersonas = horaPersonas + datetime.timedelta(minutes=1)	
        #Cantidad de personas entre 0 y 10			
		cantidadPersonas = int(np.random.uniform(0, 10))

		if cantidadPersonas > 5:

			#Mensaje si la cantidad de personas es mayor a 5
			mensajePersonas = "ALERTA hay mas de 5 personas en la habitacion"

			payload = {
				#Dato "Soy" para poder manejar el insertar en la BD
				"Soy": "Persona",
				"Fecha Personas": str(horaPersonas),
				"Cantidad Personas": str(cantidadPersonas),
				"Mensaje Personas": mensajePersonas
			}
		else: 
			#Mensaje si la catidad de personas en menor a 6
			mensajePersonas = "La cantidad de personas en la sala es aceptable"

			payload = {
				#Dato "Soy" para poder manejar el insertar en la BD
				"Soy": "Persona",
				"Fecha Personas": str(horaPersonas),
				"Cantidad Personas": str(cantidadPersonas),
				"Mensaje Personas": mensajePersonas
			}

        #Canal
		client.publish('casa/sala/personas',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)

        
if __name__ == '__main__':
	main()
	sys.exit(0)