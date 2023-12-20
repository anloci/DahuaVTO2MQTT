FROM python:3.12-alpine
MAINTAINER Elad Bar <elad.bar@hotmail.com>

WORKDIR /app

COPY . ./

RUN apk update && \
    apk upgrade && \
    pip install -r /app/requirements.txt

ENV DAHUA_VTO_HOST=vto-host
ENV DAHUA_VTO_USERNAME=Username
ENV DAHUA_VTO_PASSWORD=Password
ENV MQTT_BROKER_HOST=mqtt-host
ENV MQTT_BROKER_PORT=1883
ENV MQTT_BROKER_USERNAME=Username
ENV MQTT_BROKER_PASSWORD=Password
ENV MQTT_BROKER_TOPIC_PREFIX=DahuaVTO
ENV MQTT_BROKER_CLIENT_ID=DahuaVTO2MQTT
ENV EXPORTER_PORT=9563

RUN chmod +x /app/DahuaVTO.py
RUN echo "{ \"version\": \"$(date +'%Y.%m.%d').$(( $(date +"%s") - $(date -d "$today 0" "+%s") ))\" }" > /app/version.json

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:${EXPORTER_PORT}/metrics || exit 1

ENTRYPOINT ["python3", "/app/DahuaVTO.py"]