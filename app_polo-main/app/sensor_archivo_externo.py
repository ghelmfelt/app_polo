import datetime
import asyncio
from bleak import BleakClient, BleakScanner
import sys
import re
import paho.mqtt.client as mqtt
from config_mqtt import *
import main_externo

client_mqtt = mqtt.Client()
client_mqtt.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

uuid = '00002a37-0000-1000-8000-00805f9b34fb' # heart_rate_measurement

def process_heart_rate(queue):
    while(True):
        asyncio.run(cardiaco())

def heart_rate_callback(handle, data):

    ########## Esto es para poder enviar los datos del sensor junto a los del GPS ##########
    main_externo.q.put(f'{{"Dev{sensor_num}":{{"HR":{data[1]}}}}}') 
    ########################################################################################
    
    datos = f'{{"Dev{sensor_num}":{{"HR":{data[1]}}}}}'
    #client_mqtt.publish(MQTT_TOPIC, datos)
    print(f'{datos} ---> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def exit_handler(client, sig, frame):
    client.disconnect()
    sys.exit(0)

async def cardiaco():

    try:

        global sensor_num
        
        sensores = {
        "A0:9E:1A:23:03:AB":"Dev1",
        "A0:9E:1A:3F:39:16":"Dev2",
        "A0:9E:1A:53:7E:6F":"Dev3"
        }

        devices = BleakScanner()
        await devices.start()
        await asyncio.sleep(1)
        await devices.stop()   

        usb_detectados = devices.discovered_devices_and_advertisement_data.keys()
        sensores_detectados = [i for i in usb_detectados if i in sensores.keys()]
        sensor = sensores_detectados[0]
        
        print('Sensores detectados --->',sensor)
        sensor_num = ''.join(re.findall('\d+',sensores[sensor]))

        async with BleakClient(sensor) as client:
            print('Sensor conectado?',client.is_connected)

            rssi = devices.discovered_devices_and_advertisement_data[sensor][1].rssi
            while(rssi < 80):
                await client.start_notify(uuid, heart_rate_callback) #se desconecta automaticamente cuando sale de este bloque
                await client.stop_notify(uuid)

            await client.stop_notify(uuid)
            print(f'Lejos ---> RSSI = {rssi}')


    except Exception as e:
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} -> Ningun sensor conectado...{e}') # Ver que mostrar con este error.
        await asyncio.sleep(5)

