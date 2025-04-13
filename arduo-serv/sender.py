#!/usr/bin/env python
import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = int(os.environ["MQTT_PORT"])
MQTT_TOPIC = os.environ["MQTT_TOPIC"]

THINGSBOARD_HOST = 'arduo.es'
ACCESS_TOKEN = 'vbfeP7fXSXwXvgN8ujPs'

thingsboard_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
thingsboard_client.username_pw_set(ACCESS_TOKEN)
thingsboard_client.connect(THINGSBOARD_HOST, 1883, 60)
thingsboard_client.loop_start()

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        if "object" in payload:
            data = payload["object"]
            for key, value in data.items():
                sensor_data = {key: value}
                print(f"Enviando a ThingsBoard: {sensor_data}")
                thingsboard_client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), qos=1)
        else:
            print("No se encontró la clave 'object' en el mensaje recibido.")
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Conectado a MQTT local (código: {reason_code})")
    client.subscribe(MQTT_TOPIC)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
