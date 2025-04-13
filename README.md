# Integrated IoT, LoRaWAN, and Telemetry Project

This project integrates multiple services in a Docker environment to manage IoT devices, MQTT communication, and data visualization and storage. The solution combines:

- **Chirpstack**: LoRaWAN network server for managing devices and gateways.
- **Mosquitto**: MQTT broker for communication between devices and other services.
- **Arduo Service (arduo-serv)**: Custom service that subscribes to an MQTT topic, processes JSON messages, and sends individual variables to ThingsBoard.
- **MQTT Subscriber**: Additional service to subscribe to MQTT topics and perform actions based on configuration.
- **Data Storage and Management**:
  - **Postgres**: Database for Chirpstack.
  - **Redis**: Cache for Chirpstack services.
  - **InfluxDB**: Time-series database used by Telegraf to store telemetry data.
  - **MySQL (mqtt_db)**: MQTT-related data database (with phpMyAdmin for administration).
- **Visualization**:
  - **Grafana**: Data visualization platform for building interactive dashboards.
- **Telemetry**:
  - **Telegraf**: Metrics collection agent that sends data to InfluxDB.

This solution provides a complete architecture to manage a LoRaWAN-based IoT network, process data, and forward it to visualization and analytics platforms.

## Table of Contents

- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Deploying with Docker Compose](#deploying-with-docker-compose)
- [Accessing Services](#accessing-services)
- [Common Issues](#common-issues)
- [Contributing](#contributing)
- [License](#license)

## Project Architecture

The project consists of multiple containers communicating through a Docker internal network. Key services include:

- **Chirpstack and Bridges**  
  - *chirpstack*: LoRaWAN network server.
  - *chirpstack-gateway-bridge* and *chirpstack-gateway-bridge-basicstation*: Bridges for communication between gateways and the server.
  - *chirpstack-rest-api*: REST API to interact with Chirpstack.
- **Databases**  
  - *postgres*: Used by Chirpstack.
  - *redis*: Cache for Chirpstack server.
  - *influxdb*: Telemetry data storage.
  - *mqtt_db (MySQL)*: MQTT data management database.
- **Visualization and Management**  
  - *grafana*: Dashboard and visualization platform.
  - *phpmyadmin*: Web interface for managing the MySQL database.
- **Telemetry and Monitoring**  
  - *telegraf*: Agent collecting metrics and sending them to InfluxDB.
- **Custom Services**  
  - *mqtt-subscriber*: Service subscribing to MQTT and executing specific tasks.
  - *arduo*: Custom service that receives MQTT messages and processes them with `sender.py`, forwarding variables to ThingsBoard.

## Directory Structure

```plaintext
├── configuration/
│   ├── chirpstack/                          # Chirpstack configuration
│   ├── chirpstack-gateway-bridge/           # Gateway Bridge configuration
│   ├── mosquitto/config/                    # Mosquitto broker configuration
│   └── postgresql/                          # PostgreSQL configuration
├── arduo-serv/
│   ├── sender.py                            # Script to send data to ThingsBoard
│   ├── requirements.txt                     # Python dependencies
│   └── Dockerfile                           # Dockerfile to build Arduo image
├── sub-serv/
│   ├── subscriber.py                        # Script to send data
│   ├── requirements.txt                     # Python dependencies
│   └── Dockerfile                           # Dockerfile to build Arduo image
├── grafana/
│   ├── dashboards/                          # Custom dashboards
│   └── provisioning/                        # Datasource and panel configs
├── telegraf/
│   └── telegraf.conf                        # Telegraf configuration file
├── mysql/
│   └── init.sql                             # MySQL initialization script
├── .env                                     # Environment variables file
└── docker-compose.yaml                      # Container and service definitions
```

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- Configuration files and scripts are available in the listed directories.

## Environment Variables

This project uses environment variables defined in a `.env` file.  
⚠️ **For security and privacy reasons, specific values are not included in this repository.**

> It's recommended to provide a `.env.example` file to help other developers know which variables are needed without exposing sensitive data.

## Deploying with Docker Compose

```bash
docker-compose up --build -d
```

This command:

- Builds the custom images for `arduo` and `mqtt-subscriber`.
- Pulls official images for Chirpstack, Mosquitto, Grafana, InfluxDB, etc.
- Starts all containers defined in `docker-compose.yaml`.

## Accessing Services

- **Chirpstack** → [http://localhost:8080](http://localhost:8080)  
- **Chirpstack REST API** → [http://localhost:8090](http://localhost:8090)  
- **Grafana** → [http://localhost:3000](http://localhost:3000)  
- **InfluxDB** → [http://localhost:8086](http://localhost:8086)  
- **phpMyAdmin** → [http://localhost:8081](http://localhost:8081)  
- **MQTT Broker (Mosquitto)**: Port 1883 / WebSocket on 9001  
- **Arduo Service**: Check logs with `docker logs -f arduo` to ensure it's working  
- **MQTT Subscriber**: Subscribes to topics and processes data according to configuration  

## Common Issues

- Double-check hostnames/ports in `.env`.
- Remove volumes to reset persistent data (`docker volume rm volume_name`).
- Make sure to use `callback_api_version` when using `paho-mqtt` 2.0.0 clients.

## Contributing

Contributions are welcome. Feel free to open issues or pull requests to improve this project.

## License

This software is provided under a **restricted license**.

```text
Permission Required License

Copyright (c) 2025 Marcos Daller

All rights reserved.

This software and its associated configuration files (the "Software") may **not** be used, copied, modified, published, or distributed without **prior written permission** from the author.

Usage is restricted under the following terms:

- You must request permission via email before using or deploying any part of the Software.
- Upon approval, the author will provide a sample `.env` file with the required variables for configuration.
- The Software may not be used for commercial or academic purposes without explicit consent.
- Redistribution or sublicensing is prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

To request permission, contact: m.daller.2018@alumnos.urjc.es

```
