		# Laboratorio 2: IoT MQTT y Plotly
		# Alumna: Nicole Brito Strusi
		# Carnet: 20181110056


# PUBLICACIÓN DE BAÑO


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
def ultima_fecha_bano():
	try:
		#Conexión con la BD
		conexion = conexionBD.get_connection()
		cursor = conexion.cursor()
		query = """SELECT fecha_tanque FROM public.bano ORDER BY ID DESC LIMIT 1;"""
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
    client = paho.mqtt.client.Client("Bano", False)
    #Calidad del Servicio
    client.qos = 0
    #Conexión
    client.connect(host='localhost')

    #Datos para el baño

    #Media y Desviación
    mediaTanqueMenos=0.1    
    mediaTanqueMas = 0.2
    desviacionTanqueMenos = 0.05
    desviacionTanqueMas = 0.05

    #Tanque cantidad de agua inicial
    tanque = 100

    #Para calcular los 30 minutos que pasan para cuando entra el agua
    contador = 0

    #Hora Base Tanque
    horaTanque = ultima_fecha_bano()
    
    while(True):
        #TANQUE:

        #Aumento del contador
        contador = contador + 1

        #Cálculo de la desviación para disminuir tanque
        cantidadTanqueMenos = np.random.normal(mediaTanqueMenos * 100, desviacionTanqueMenos * 100)
        
        #Si la cantidad de agua que sale del tanque es negativa
        if (tanque - cantidadTanqueMenos) < 0:
            tanque = 0
        else:
            #Disminuir cantidad de tanque 
            tanque = tanque - cantidadTanqueMenos

        #Aumento de 10 minutos
        horaTanque = horaTanque + datetime.timedelta(minutes=10)

        if contador == 3 :
            #Reinicio del contador
            contador = 0

            #Cálculo de la desviación para aumentar tanque
            cantidadTanqueMas = np.random.normal(mediaTanqueMas * 100, desviacionTanqueMas * 100)
            
            #Si la cantidad de agua que entra supera la capacidad del tanque
            if (cantidadTanqueMas + tanque) > 100:
                tanque = 100
            else:
                #Aumento de la cantidad del tanque
                tanque = tanque + cantidadTanqueMas
        
        if tanque > 0 and tanque <= 50:
            #Mensaje si el tannque tiene entre 1 y 50 de capacidad
            mensajeBano = "ALERTA La cantidad de agua es crítica"

            payload = {
                "Fecha Tanque": str(horaTanque),
                "Tanque": str(tanque),
                "Mensaje Bano": mensajeBano
            }

        elif tanque ==0:
            #Mensaje si el tanque no tiene agua
            mensajeBano = "ALERTA La cantidad de agua es CERO"
            
            payload = {
                "Fecha Tanque": str(horaTanque),
                "Tanque": str(tanque),
                "Mensaje Bano": mensajeBano
		    }

        else:
             #Mensaje si la cantidad de agua es superior a 50
            mensajeBano = "La cantidad de agua esta bien"

            payload = {
                "Fecha Tanque": str(horaTanque),
                "Tanque": str(tanque),
                "Mensaje Bano": mensajeBano
		    }

        #Canal
        client.publish('casa/bano',json.dumps(payload),qos=0)
        #Imprimir mensaje
        print(payload)
        #Tiempo para publicación de mensajes
        time.sleep(0.5)

        
        

if __name__ == '__main__':
	main()
	sys.exit(0)