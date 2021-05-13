		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# PUBLICACIÓN DE ALEXA


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

#Importaciones API
import requests

#Importaciones para la BD

import psycopg2
import conexionBD
import json

#Def para obtener el ultimo tiempo que se necesita para insertar el siguiente dato
def ultima_fecha_alexa():
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """SELECT fecha_alexa FROM public.alexa ORDER BY ID DESC LIMIT 1;"""
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
	client = paho.mqtt.client.Client("Alexa", False)
    #Calidad del Servicio
	client.qos = 0
    #Conexión
	client.connect(host='localhost')

    #Hora Base Alexa
	horaAlexa = ultima_fecha_alexa()

	while(True):

        #ALEXA:

        #Aumento de 1 hora
		horaAlexa = horaAlexa + datetime.timedelta(hours=1)	
        #API para la temperatura de Caracas en grados centígrados
		baseURL = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Caracas&appid=f04a601ea513154506ae21463e41adf6&units=metric")
		#Obtener data 
		data = baseURL.json()
		main = data['main']
		#Obtener temperatura Caracas
		temperaturaAlexa = main['temp']
		#Mensaje 
		payload = {
			#Dato "Soy" para poder manejar el insertar en la BD
			"Soy": "Alexa",
			"Fecha Alexa": str(horaAlexa),
			"Temperatura Caracas": str(temperaturaAlexa)
		}

        #Canal
		client.publish('casa/sala/alexa',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)

        
if __name__ == '__main__':
	main()
	sys.exit(0)