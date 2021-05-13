		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# SUSCRIPTOR DE LA SALA DE LA CASA


#Importaciones
import sys
import paho.mqtt.client

#BASE DE DATOS

#Importaciones para la BD

import psycopg2
import conexionBD
import json


#Para insertar en la BD los datos de las personas de la sala
def insertar_personas(fecha, personas, mensaje):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.personas(fecha_personas, cantidad_personas, mensaje_personas) VALUES (%s, %s, %s);"""
		cursor.execute(query,(fecha,personas, mensaje))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)

#Para insertar en la BD los datos de Alexa
def insertar_alexa(fecha, alexa):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.alexa(fecha_alexa, temperatura_alexa) VALUES (%s, %s);"""
		cursor.execute(query,(fecha, alexa))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)


#Canal al que se suscribe, en este caso, a la sala de la casa
def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/sala/#', qos=2)

#Mensajes que escucha
def on_message(client, userdata, message):
	print('------------------------------')
	print('Tópico: %s' % message.topic)
	print('Mensaje: %s' % message.payload)
	print('QOS: %d' % message.qos)

	#Dependiendo del parámetro "Soy" pasado por el payload hace:
	
	if json.loads(message.payload)["Soy"] == "Persona":
		#Insertando datos en la BD las personas de la sala
		insertar_personas(json.loads(message.payload)["Fecha Personas"], json.loads(message.payload)["Cantidad Personas"], json.loads(message.payload)["Mensaje Personas"])
	if json.loads(message.payload)["Soy"] == "Alexa":
		#Insertando datos en la BD de Alexa
		insertar_alexa(json.loads(message.payload)["Fecha Alexa"], json.loads(message.payload)["Temperatura Caracas"])
	

def main():
	#Cliente
	client = paho.mqtt.client.Client(client_id='sala-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)