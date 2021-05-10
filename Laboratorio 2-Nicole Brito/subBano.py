		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# SUSCRIPTOR DEL BAÑO DE LA CASA


#Importaciones
import sys
import paho.mqtt.client

#BASE DE DATOS

#Importaciones para la BD

import psycopg2
import conexionBD
import json


#Para insertar en la BD los datos del baño
def insertar_bano(fecha, tanque, mensaje):
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """INSERT INTO public.bano(fecha_tanque, tanque, mensaje_tanque) VALUES (%s, %s, %s);"""
		cursor.execute(query,(fecha,tanque, mensaje))
		#Para que se vea reflejado en la BD
		conexion.commit()
		#res = cursor.fetchone()
		conexionBD.close_connection(conexion)
	except (Exception, psycopg2.Error) as error:
		print('Error obteniendo la data',error)


#Canal al que se suscribe, en este caso, al baño de la casa
def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/bano', qos=2)

#Mensajes que escucha
def on_message(client, userdata, message):
	print('------------------------------')
	print('Tópico: %s' % message.topic)
	print('Mensaje: %s' % message.payload)
	print('QOS: %d' % message.qos)
	
	#Insertando datos en la BD del baño
	insertar_bano(json.loads(message.payload)["Fecha Tanque"], json.loads(message.payload)["Tanque"], json.loads(message.payload)["Mensaje Bano"])


def main():
	#Cliente
	client = paho.mqtt.client.Client(client_id='bano-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)