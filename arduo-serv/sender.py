#!/usr/bin/env python
import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del broker MQTT local
MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = int(os.environ["MQTT_PORT"])
MQTT_TOPIC = os.environ["MQTT_TOPIC"]

# Configuración de ThingsBoard
THINGSBOARD_HOST = 'arduo.es'
ACCESS_TOKEN = 'vbfeP7fXSXwXvgN8ujPs'  # Reemplaza con tu token

# Crear cliente para ThingsBoard con callback_api_version requerido
thingsboard_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
thingsboard_client.username_pw_set(ACCESS_TOKEN)
thingsboard_client.connect(THINGSBOARD_HOST, 1883, 60)
thingsboard_client.loop_start()

# Callback de recepción de mensajes del broker MQTT local
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        if "object" in payload:
            data = payload["object"]
            # Enviar cada variable encontrada bajo "object" por separado a ThingsBoard
            for key, value in data.items():
                sensor_data = {key: value}
                print(f"Enviando a ThingsBoard: {sensor_data}")
                thingsboard_client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), qos=1)
        else:
            print("No se encontró la clave 'object' en el mensaje recibido.")
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

# Callback de conexión del broker MQTT local
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Conectado a MQTT local (código: {reason_code})")
    client.subscribe(MQTT_TOPIC)

# Crear cliente para el broker MQTT local con callback_api_version requerido
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
