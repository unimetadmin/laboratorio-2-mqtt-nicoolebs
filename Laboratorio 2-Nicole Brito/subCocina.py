		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# SUSCRIPTOR DE LA COCINA DE LA CASA


#Importaciones
import sys
import paho.mqtt.client


#BASE DE DATOS

#Importaciones para la BD

import psycopg2
import conexionBD
import json

#Para insertar en la BD los datos de la nevera - Temperatura
def insertar_nevera(fecha, temperatura):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.nevera(fecha_temperatura, temperatura) VALUES (%s,%s);"""
		cursor.execute(query,(fecha,temperatura))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)

#Para insertar en la BD los datos de los Hielos - nevera
def insertar_hielo(fecha, hielo):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.hielo(fecha_hielo, hielo) VALUES (%s, %s);"""
		cursor.execute(query,(fecha,hielo))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)

#Para insertar en la BD los datos de la Olla
def insertar_olla(fecha, olla, mensaje):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.olla(fecha_olla, olla, mensaje_olla) VALUES (%s, %s, %s);"""
		cursor.execute(query,(fecha,olla,mensaje))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)


#Canal al que se suscribe, en este caso, a la cocina de la casa
def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/cocina/#', qos=2)

#Mensajes que escucha y publica en la BD los datos
def on_message(client, userdata, message):
	print('------------------------------')
	print('Tópico: %s' % message.topic)
	print('Mensaje: %s' % message.payload)
	print('QOS: %d' % message.qos)

	#Dependiendo del parámetro "Soy" pasado por el payload hace:
	
	if json.loads(message.payload)["Soy"] == "Temperatura":
		#Insertando datos en la BD de la temperatura de la nevera
		insertar_nevera(json.loads(message.payload)["Fecha Temperatura"], json.loads(message.payload)["Temperatura"])
	if json.loads(message.payload)["Soy"] == "Hielo":
		#Insertando datos en la BD de los hielos de la nevera
		insertar_hielo(json.loads(message.payload)["Fecha Hielo"], json.loads(message.payload)["Hielo"])
	if json.loads(message.payload)["Soy"] == "Olla":
		#Insertando datos en la BD de la olla
		insertar_olla(json.loads(message.payload)["Fecha Temperatura Olla"], json.loads(message.payload)["Temperatura Olla"],json.loads(message.payload)["Mensaje Olla"])
	
	

def main():
	#Cliente
	client = paho.mqtt.client.Client(client_id='cocina-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)