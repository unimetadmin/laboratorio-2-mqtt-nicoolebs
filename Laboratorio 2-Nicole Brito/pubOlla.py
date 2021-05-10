		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# PUBLICACIÓN DE LA OLLA - TEMPERATURA


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
def ultima_fecha_olla():
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """SELECT fecha_olla FROM public.olla ORDER BY ID DESC LIMIT 1;"""
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
	client = paho.mqtt.client.Client("Olla", False)
    #Calidad del Servicio
	client.qos = 0
    #Conexión
	client.connect(host='localhost')

    #Hora Base Olla
	horaOlla = ultima_fecha_olla()

	while(True):

        #OLLA:

        #Aumento de 1 segundo 
		horaOlla = horaOlla + datetime.timedelta(seconds=1)	
        #Temperatura Olla entre 0 y 150			
		temperaturaOlla = int(np.random.uniform(0, 150))

		if temperaturaOlla >=100:

			#Mensaje si la temperatura es mayor o igual a 100 grados
			mensajeOlla = "El agua ya hirvio"

			payload = {
				#Dato "Soy" para poder manejar el insertar en la BD
				"Soy": "Olla",
				"Fecha Temperatura Olla": str(horaOlla),
				"Temperatura Olla": str(temperaturaOlla),
				"Mensaje Olla":mensajeOlla
			}
		else: 
			#Mensaje si la temperatura es menor a 100 grados
			mensajeOlla = "El agua no ha hervido"

			payload = {
				#Dato "Soy" para poder manejar el insertar en la BD
				"Soy": "Olla",
				"Fecha Temperatura Olla": str(horaOlla),
				"Temperatura Olla": str(temperaturaOlla),
				"Mensaje Olla":mensajeOlla
			}

        #Canal
		client.publish('casa/cocina/olla',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)

        
if __name__ == '__main__':
	main()
	sys.exit(0)