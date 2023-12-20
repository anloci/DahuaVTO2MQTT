# DahuaVTO2MQTT
Listens to events from all Dahua devices - VTO, Camera, NVR unit and publishes them via MQTT Message

[Change log](https://gitlab.com/elad.bar/DahuaVTO2MQTT/-/blob/master/CHANGELOG.md)

[Dahua VTO MQTT Events - examples](https://gitlab.com/elad.bar/DahuaVTO2MQTT/-/blob/master/MQTTEvents.MD)

## How to install
### Docker Compose
```dockercompose
version: '3'
services:
  dahuavto2mqtt:
    image: "registry.gitlab.com/elad.bar/dahuavto2mqtt:latest"
    container_name: "dahuavto2mqtt"
    hostname: "dahuavto2mqtt"
    restart: "unless-stopped"
    environment:
      - DAHUA_VTO_HOST=vto-host
      - DAHUA_VTO_USERNAME=Username
      - DAHUA_VTO_PASSWORD=Password
      - MQTT_BROKER_HOST=mqtt-host
      - MQTT_BROKER_PORT=1883
      - MQTT_BROKER_USERNAME=Username
      - MQTT_BROKER_PASSWORD=Password 
      - MQTT_BROKER_TOPIC_PREFIX=DahuaVTO
      - MQTT_BROKER_CLIENT_ID=DahuaVTO2MQTT
      - EXPORTER_PORT=9563
      - DEBUG=False
```

### Environment Variables
| Variable                 | Default       | Required | Description                 |
|--------------------------|---------------|----------|-----------------------------|
| DAHUA_VTO_HOST           | -             | +        | Dahua VTO hostname or IP    |
| DAHUA_VTO_USERNAME       | -             | +        | Dahua VTO user name         |
| DAHUA_VTO_PASSWORD       | -             | +        | Dahua VTO password          |
| MQTT_BROKER_HOST         | -             | +        | MQTT Broker hostname or IP  |
| MQTT_BROKER_PORT         | -             | +        | MQTT Broker port            |
| MQTT_BROKER_USERNAME     | -             | +        | MQTT Broker user name       |
| MQTT_BROKER_PASSWORD     | -             | +        | MQTT Broker password        |
| MQTT_BROKER_TOPIC_PREFIX | DahuaVTO      | -        | Topic to publish messages   |
| MQTT_BROKER_CLIENT_ID    | DahuaVTO2MQTT | -        | MQTT Broker client ID       |
| EXPORTER_PORT            | 9563          | -        | Port for Promethus exporter |
| DEBUG                    | false         | -        | Enable debug log messages   |

## Commands

#### Open Door
By publishing MQTT message of {MQTT_BROKER_TOPIC_PREFIX}/Command/Open an HTTP request to the unit will be sent,
If the payload of the message is empty, default door to open is 1,
If unit supports more than 1 door, please add to the payload `Door` parameter with the number of the door 

## Prometheus Exporter

`instance` is based pm MQTT Client ID, default is `DahuaVTO2MQTT`

`version` is based on the docker image, format is `Year.Month.Day.NumberOfSecondsSinceMidnight`

```prom
# HELP dahuavto2mqtt_mqtt_status MQTT Connectivity Status
# TYPE dahuavto2mqtt_mqtt_status gauge
dahuavto2mqtt_mqtt_status{instance="DahuaVTO2MQTT",version="2023.12.20.35999"} 1.0
# HELP dahuavto2mqtt_mqtt_incoming_messages MQTT Incoming Messages
# TYPE dahuavto2mqtt_mqtt_incoming_messages gauge
dahuavto2mqtt_mqtt_incoming_messages{instance="DahuaVTO2MQTT",topic="Command/Open",version="2023.12.20.35999"} 2.0
# HELP dahuavto2mqtt_mqtt_outgoing_messages MQTT Outgoing Messages
# TYPE dahuavto2mqtt_mqtt_outgoing_messages gauge
dahuavto2mqtt_mqtt_outgoing_messages{instance="DahuaVTO2MQTT",topic="AlarmLocal/Event",version="2023.12.20.35999"} 2.0
# HELP dahuavto2mqtt_mqtt_failed_outgoing_messages MQTT Failed Outgoing Messages
# TYPE dahuavto2mqtt_mqtt_failed_outgoing_messages gauge
# HELP dahuavto2mqtt_dahua_status Dahua Connectivity Status
# TYPE dahuavto2mqtt_dahua_status gauge
dahuavto2mqtt_dahua_status{instance="DahuaVTO2MQTT",version="2023.12.20.35999"} 1.0
# HELP dahuavto2mqtt_dahua_messages Dahua Messages
# TYPE dahuavto2mqtt_dahua_messages gauge
dahuavto2mqtt_dahua_messages{instance="DahuaVTO2MQTT",session_id="0",topic="global.login",version="2023.12.20.35999"} 1.0
# HELP dahuavto2mqtt_dahua_failed_messages Dahua Failed Messages
# TYPE dahuavto2mqtt_dahua_failed_messages gauge
dahuavto2mqtt_dahua_failed_messages{instance="DahuaVTO2MQTT",session_id="0",topic="incoming",version="2023.12.20.35999"} 1.0
```

## Credits
All credits goes to <a href="https://github.com/riogrande75">@riogrande75</a> who wrote that complicated integration
Original code can be found in <a href="https://github.com/riogrande75/Dahua">@riogrande75/Dahua</a>
