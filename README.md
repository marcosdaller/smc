# Proyecto Integrado de IoT, LoRaWAN y Telemetría

Este proyecto integra múltiples servicios en un entorno Docker para gestionar dispositivos IoT, comunicaciones MQTT y la visualización y almacenamiento de datos. La solución combina:

- **Chirpstack**: Servidor de red LoRaWAN que permite la gestión de dispositivos y gateways.
- **Mosquitto**: Broker MQTT para la comunicación entre dispositivos y otros servicios.
- **Arduo Service (arduo-serv)**: Servicio personalizado que se suscribe a un tópico MQTT, procesa mensajes JSON y envía variables individualmente a ThingsBoard.
- **MQTT Subscriber**: Servicio adicional para suscribirse a tópicos MQTT y realizar acciones según la configuración.
- **Almacenamiento y Gestión de Datos**:
  - **Postgres**: Base de datos para Chirpstack.
  - **Redis**: Caché para los servicios de Chirpstack.
  - **InfluxDB**: Base de datos de series temporales utilizada por Telegraf para almacenar telemetría.
  - **MySQL (mqtt_db)**: Base de datos para otros datos relacionados con MQTT (con phpMyAdmin para administración).
- **Visualización**:
  - **Grafana**: Plataforma de visualización de datos para crear dashboards interactivos.
- **Telemetría**:
  - **Telegraf**: Agente para la recolección de métricas que envía datos a InfluxDB.

Esta solución ofrece una arquitectura completa para gestionar una red IoT basada en LoRaWAN, procesar y enviar datos a plataformas de visualización y análisis.

## Tabla de Contenidos

- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Estructura de Directorios](#estructura-de-directorios)
- [Requisitos Previos](#requisitos-previos)
- [Variables de Entorno](#variables-de-entorno)
- [Despliegue con Docker Compose](#despliegue-con-docker-compose)
- [Acceso a los Servicios](#acceso-a-los-servicios)
- [Problemas Comunes](#problemas-comunes)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Arquitectura del Proyecto

El proyecto se compone de múltiples contenedores que se comunican mediante una red interna de Docker. A continuación, se listan los servicios clave:

- **Chirpstack y sus puentes**  
  - *chirpstack*: Servidor de red LoRaWAN.
  - *chirpstack-gateway-bridge* y *chirpstack-gateway-bridge-basicstation*: Puentes para la comunicación entre los gateways y el servidor.
  - *chirpstack-rest-api*: API REST para interactuar con Chirpstack.
- **Bases de Datos**  
  - *postgres*: Utilizado por Chirpstack.
  - *redis*: Caché para el servidor Chirpstack.
  - *influxdb*: Repositorio de datos de telemetría.
  - *mqtt_db (MySQL)*: Base de datos para la gestión de datos MQTT.
- **Visualización y Administración**  
  - *grafana*: Plataforma de dashboards y visualización.
  - *phpmyadmin*: Interfaz web para administrar la base de datos MySQL.
- **Telemetría y Monitoreo**  
  - *telegraf*: Agente que recolecta métricas y las envía a InfluxDB.
- **Servicios Personalizados**  
  - *mqtt-subscriber*: Servicio que se suscribe a MQTT y realiza tareas específicas.
  - *arduo*: Servicio personalizado que recibe mensajes MQTT y, mediante el script `sender.py`, procesa y reenvía variables a ThingsBoard.

## Estructura de Directorios

```plaintext
├── configuration/
│   ├── chirpstack/                          # Configuraciones de Chirpstack
│   ├── chirpstack-gateway-bridge/           # Configuraciones del Gateway Bridge
│   ├── mosquitto/config/                    # Configuraciones del broker Mosquitto
│   └── postgresql/                          # Configuraciones del postgresql
├── arduo-serv/
│   ├── sender.py                            # Script que envía datos a ThingsBoard
│   ├── requirements.txt                     # Dependencias de Python
│   └── Dockerfile                           # Dockerfile para construir la imagen de Arduo
├── sub-serv/                                
│   ├── subscriber.py                        # Script que envía datos
│   ├── requirements.txt                     # Dependencias de Python
│   └── Dockerfile                           # Dockerfile para construir la imagen de Arduo
├── grafana/
│   ├── dashboards/                          # Dashboards personalizados
│   └── provisioning/                        # Configuraciones de datasources y paneles
├── telegraf/
│   └── telegraf.conf                        # Archivo de configuración para Telegraf
├── mysql/
│   └── init.sql                             # Script de inicialización para MySQL
├── .env                                     # Archivo de variables de entorno
└── docker-compose.yaml                      # Definición de contenedores y servicios
```

## Requisitos Previos

- **Docker**: [Instalación de Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instalación de Docker Compose](https://docs.docker.com/compose/install/)
- Archivos de configuración y scripts disponibles en las carpetas indicadas.

## Variables de Entorno

El proyecto hace uso de variables de entorno definidas en un archivo `.env`.  
⚠️ **Por motivos de seguridad y privacidad, el contenido específico de estas variables no se incluye en este repositorio.**

> Se recomienda proporcionar un archivo `.env.example` para que otros desarrolladores puedan saber qué variables deben definir sin revelar valores sensibles.

## Despliegue con Docker Compose

```bash
docker-compose up --build -d
```

Este comando:

- Construirá las imágenes personalizadas para `arduo` y `mqtt-subscriber`.
- Descargará las imágenes oficiales de Chirpstack, Mosquitto, Grafana, InfluxDB, etc.
- Levantará todos los contenedores definidos en `docker-compose.yaml`.

## Acceso a los Servicios

- **Chirpstack** → [http://localhost:8080](http://localhost:8080)  
- **Chirpstack REST API** → [http://localhost:8090](http://localhost:8090)  
- **Grafana** → [http://localhost:3000](http://localhost:3000)  
- **InfluxDB** → [http://localhost:8086](http://localhost:8086)  
- **phpMyAdmin** → [http://localhost:8081](http://localhost:8081)  
- **Broker MQTT (Mosquitto)**: Puerto 1883 / WebSocket en 9001  
- **Servicio Arduo**: Verifica los logs con `docker logs -f arduo` para asegurar funcionamiento  
- **MQTT Subscriber**: Suscripción a tópicos y procesamiento según configuración  

## Problemas Comunes

- Verifica los nombres de host/puertos en `.env`.
- Elimina volúmenes si necesitas reiniciar datos persistentes (`docker volume rm nombre_volumen`).
- Asegúrate de usar `callback_api_version` en clientes MQTT con `paho-mqtt 2.0.0`.

## Contribuciones

Las contribuciones son bienvenidas. Puedes abrir issues o pull requests para mejorar este proyecto.

## Licencia

Este software se entrega **solo para fines de visualización y referencia**.

```text
Restricted Viewing License

Copyright (c) 2025 Marcos Daller

All rights reserved.

This software and its associated documentation files (the "Software") are
provided for viewing purposes only. Permission is hereby granted to any
person obtaining a copy of this Software to view its contents privately,
for informational or educational reference only, under the following conditions:

- The Software may not be used, copied, modified, merged, published,
  distributed, sublicensed, sold, or executed in any environment.
- The Software may not be used for commercial, academic, or personal
  projects.
- No rights of usage, distribution, or modification are granted, even if 
  explicit permission is given by the author. All access is strictly for review.

THE SOFTWARE IS PROVIDED "AS IS", FOR REFERENCE ONLY, WITHOUT ANY WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO 
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE VIEWING OF THE SOFTWARE.

To request permission for any kind of use beyond viewing, contact: [tu_email@ejemplo.com]
```
