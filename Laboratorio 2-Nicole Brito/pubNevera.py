		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# PUBLICACIÓN DE NEVERA - HIELO Y TEMPERATURA 


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
def ultima_fecha_nevera():
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """SELECT fecha_temperatura FROM public.nevera ORDER BY ID DESC LIMIT 1;"""
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
	client = paho.mqtt.client.Client("Nevera", False)
    #Calidad del Servicio
	client.qos = 0
    #Conexión
	client.connect(host='localhost')

    #Datos para la Temperatura

    #Media
	mediaTemperatura = 10
    #Desviación 
	desviacionTemperatura = 2
    
    #Cálculo de la desviación
	temperaturaPorMinutos = np.random.normal(mediaTemperatura, desviacionTemperatura)

    #Hora Base Temperatura
	horaTemperatura = ultima_fecha_nevera()

	while(temperaturaPorMinutos > 0):
		
		#TEMPERATURA 1: 

        #Aumento de 5 minutos
		horaTemperatura = horaTemperatura + datetime.timedelta(minutes=5)	
        #Temperatura entre 8 y 12			
		temperatura = int(np.random.uniform(8, 12))

        #Mensaje
		payload = {
			#Dato "Soy" para poder manejar el insertar en la BD
			"Soy": "Temperatura",
			"Fecha Temperatura": str(horaTemperatura),
			"Temperatura": str(temperatura)
		}

        #Canal
		client.publish('casa/cocina/nevera',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)

        #TEMPERATURA 2: 

        #Aumento de 5 minutos
		horaTemperatura = horaTemperatura + datetime.timedelta(minutes=5)	
        #Temperatura entre 8 y 12			
		temperatura = int(np.random.uniform(8, 12))

        #Mensaje
		payload = {
			#Dato "Soy" para poder manejar el insertar en la BD
			"Soy": "Temperatura",
			"Fecha Temperatura": str(horaTemperatura),
			"Temperatura": str(temperatura)
		}

        #Canal
		client.publish('casa/cocina/nevera',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)
		
		#HIELO:

		#Hora del hielo
		horaHielo = horaTemperatura
		#Hielo entre 0 y 10
		hielo= int(np.random.uniform(0, 10))

        #Mensaje
		payload = {
			#Dato "Soy" para poder manejar el insertar en la BD
			"Soy": "Hielo",
			"Fecha Hielo": str(horaHielo),
			"Hielo": str(hielo)
		}

        #Canal
		client.publish('casa/cocina/nevera',json.dumps(payload),qos=0)		
        #Imprimir mensaje
		print(payload)
        #Tiempo para publicación de mensajes
		time.sleep(0.5)


if __name__ == '__main__':
	main()
	sys.exit(0)