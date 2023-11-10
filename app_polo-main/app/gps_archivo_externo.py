import time
import serial
import datetime
from geopy import distance
import paho.mqtt.client as mqtt
from config_mqtt import *
import re
import main_externo


client_mqtt = mqtt.Client()
client_mqtt.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# ------------- Funciones y definiciones GPS ----------------

def getFormattedLatitude(lat, direction):
    if lat == '':
        return 'No-data'
    else:
        latDegrees = int(float(lat)/100)
        latMinutes = float(lat) - latDegrees * 100
        fixedLat = latDegrees + latMinutes/60
        return fixedLat if str(direction) == 'N' else (fixedLat * -1)

def getFormattedLongitude(lon, direction):
    if lon == '':
        return 'No-data'
    else:
        lonDegrees = int(float(lon)/100)
        lonMinutes = float(lon) - lonDegrees * 100
        fixedLon = lonDegrees + lonMinutes/60
        return fixedLon if str(direction) == 'E' else (fixedLon * -1)

def getDistanceBetween2Points(p1, p2):
    if not p1 or not p2:
        return 0
    if 'No-data' in p1 or 'No-data' in p2:
        return 0
    return distance.distance(p1, p2).km


def getGPSData(ser):
    
    buffer = ""
    while True:
        oneByte = ser.read(1)
        if oneByte == b"\r":    #method should returns bytes
            return buffer
        else:
            buffer += oneByte.decode("cp1252")


def send_data_to_mqtt(data):
    client_mqtt.publish(MQTT_TOPIC, data)


def process_gps(queue):
    previous_coordinates = None
    while(True):
        
        try:

            ser = serial.Serial(
            port='/dev/ttyAML4',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )

            maxSpeed = 0.0
            totalDistance = 0.0
 
            gps = ['','','','','','','','','','','','','']
            datos_gps = getGPSData(ser)

            if '$GPRMC' in datos_gps:
                gps = datos_gps.replace('\n','').split(',')

            res = {
            'latitude':getFormattedLatitude(gps[3], gps[4]),
            'longitude': getFormattedLongitude(gps[5], gps[6]),
            'speedOverGround': round(float(gps[7]) * 1.852, 2) if gps[7] != '' else 0
            }

            current_speed = res["speedOverGround"]
            maxSpeed = max(maxSpeed, current_speed)

            current_coordinates = 'No-data'
            if (res['latitude'] != 'No-data' and res['longitude'] != 'No-data'):
                current_coordinates = float(res['latitude']),float(res['longitude'])

            if previous_coordinates:
                totalDistance = getDistanceBetween2Points(previous_coordinates, current_coordinates) #modificado Danilo

            previous_coordinates = current_coordinates
            
            data_hr_quere = main_externo.q.get()
            sensor = ''.join(re.findall('Dev\d+',data_hr_quere))[3:]
            hr_valor = ''.join(re.findall('\:\d+',data_hr_quere))[1:]
            datos_dict = f'{{"Board1":{{"SENSOR":{sensor},"HR":{hr_valor},"DATETIME":"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}","LAT":{res["latitude"]},"LON":{res["longitude"]},"SPEED":{res["speedOverGround"]},"MAXSPEED":{maxSpeed},"TOTAL-DISTANCE":{totalDistance}}}}}'
            print(f'{datos_dict}\n')
            #####################################################################################################

            if (res['latitude'] != 'No-data' and res['longitude'] != 'No-data'):
                print(f'--> Publicar <--\n')

                client_mqtt.reconnect()
                send_data_to_mqtt(datos_dict)

            ser.close()

        except Exception as e:
            print(f'Error GPS --> {e}')
