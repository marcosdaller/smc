import os
import json
import mysql.connector
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = int(os.environ["MQTT_PORT"])
MQTT_TOPIC = os.environ["MQTT_TOPIC"]

DB_CONFIG = {
    "host": os.environ["MYSQL_HOST"],
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "database": os.environ["MYSQL_DATABASE"],
    "port": int(os.environ["MYSQL_CONTAINER_PORT"])
}

def store_in_mysql(payload: str):
    data = json.loads(payload)
    device_info = data.get("deviceInfo", {})
    rx_info = data.get("rxInfo", [])
    
    object_vars = data.get("object", {})

    if not device_info:
        return  

    tenant_id = device_info["tenantId"]
    tenant_name = device_info["tenantName"]

    application_id = device_info["applicationId"]
    application_name = device_info["applicationName"]

    device_profile_id = device_info["deviceProfileId"]
    device_profile_name = device_info["deviceProfileName"]

    dev_eui = device_info["devEui"]
    device_name = device_info["deviceName"]
    device_class = device_info["deviceClassEnabled"]

    dev_addr = data.get("devAddr")  

    gateway_id = None
    if rx_info and len(rx_info) > 0:
        gateway_id = rx_info[0].get("gatewayId")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        insert_tenant = """
            INSERT IGNORE INTO tenant (id, name)
            VALUES (%s, %s)
        """
        cursor.execute(insert_tenant, (tenant_id, tenant_name))

        insert_app = """
            INSERT IGNORE INTO application (id, tenant_id, name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_app, (application_id, tenant_id, application_name))

        insert_profile = """
            INSERT IGNORE INTO device_profile (id, tenant_id, name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_profile, (device_profile_id, tenant_id, device_profile_name))

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

        if gateway_id:
            insert_gw = """
                INSERT IGNORE INTO gateway (gateway_id, tenant_id, name)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_gw, (gateway_id, tenant_id, None))


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

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado a MQTT (código: {reason_code})")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8', errors='replace')
    store_in_mysql(payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
