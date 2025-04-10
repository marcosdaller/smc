import os
import json
import mysql.connector
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración MQTT
MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = int(os.environ["MQTT_PORT"])
MQTT_TOPIC = os.environ["MQTT_TOPIC"]

# Configuración MySQL
DB_CONFIG = {
    "host": os.environ["MYSQL_HOST"],
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "database": os.environ["MYSQL_DATABASE"],
    "port": int(os.environ["MYSQL_CONTAINER_PORT"])
}

def store_in_mysql(payload: str):
    """
    Recibe el payload JSON de ChirpStack, extrae los campos
    y los inserta en la base de datos según tu esquema.
    También inserta las variables (key) presentes en 'object'.
    """
    # Parsear el JSON
    data = json.loads(payload)
    device_info = data.get("deviceInfo", {})
    rx_info = data.get("rxInfo", [])
    
    # Este diccionario contendrá las variables en 'object'
    # Si no existe 'object', devolvemos un dict vacío
    object_vars = data.get("object", {})

    if not device_info:
        return  # No hay datos de dispositivo, salimos

    # Extraer valores
    tenant_id = device_info["tenantId"]
    tenant_name = device_info["tenantName"]

    application_id = device_info["applicationId"]
    application_name = device_info["applicationName"]

    device_profile_id = device_info["deviceProfileId"]
    device_profile_name = device_info["deviceProfileName"]

    dev_eui = device_info["devEui"]
    device_name = device_info["deviceName"]
    device_class = device_info["deviceClassEnabled"]

    dev_addr = data.get("devAddr")  # p.ej. "014c59a8"

    # rxInfo para obtener gatewayId (asumimos que usas el primer gateway)
    gateway_id = None
    if rx_info and len(rx_info) > 0:
        gateway_id = rx_info[0].get("gatewayId")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1) Insert tenant
        insert_tenant = """
            INSERT IGNORE INTO tenant (id, name)
            VALUES (%s, %s)
        """
        cursor.execute(insert_tenant, (tenant_id, tenant_name))

        # 2) Insert application
        insert_app = """
            INSERT IGNORE INTO application (id, tenant_id, name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_app, (application_id, tenant_id, application_name))

        # 3) Insert device_profile
        insert_profile = """
            INSERT IGNORE INTO device_profile (id, tenant_id, name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_profile, (device_profile_id, tenant_id, device_profile_name))

        # 4) Insert device
        insert_device = """
            INSERT IGNORE INTO device (
                dev_eui, application_id, device_profile_id,
                name, device_class, dev_addr
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_device, (
            dev_eui,
            application_id,
            device_profile_id,
            device_name,
            device_class,
            dev_addr
        ))

        # 5) Insert gateway (si existe gateway_id)
        if gateway_id:
            insert_gw = """
                INSERT IGNORE INTO gateway (gateway_id, tenant_id, name)
                VALUES (%s, %s, %s)
            """
            # Ponemos el nombre en None (o lo que consideres) ya que no viene en el payload
            cursor.execute(insert_gw, (gateway_id, tenant_id, None))

        # 6) Insert variables de 'object' en device_variable
        #    Solo se guarda el nombre de la variable (key),
        #    pues la tabla no tiene columna para el valor.
        insert_variable = """
            INSERT IGNORE INTO device_variable (dev_eui, name)
            VALUES (%s, %s)
        """
        for var_name in object_vars.keys():
            cursor.execute(insert_variable, (dev_eui, var_name))

        conn.commit()

    except mysql.connector.Error as err:
        print(f"❌ Error MySQL: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# Callbacks MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado a MQTT (código: {reason_code})")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8', errors='replace')
    # Guardar en la base de datos
    store_in_mysql(payload)

# Cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
