#!/usr/bin/env python3
import json
import os
import sys
import logging
from time import sleep

from clients.DahuaClient import DahuaClient
from clients.MQTTClient import MQTTClient
from prometheus_client import start_http_server, CollectorRegistry

DEBUG = str(os.environ.get('DEBUG', False)).lower() == str(True).lower()

log_level = logging.DEBUG if DEBUG else logging.INFO

root = logging.getLogger()
root.setLevel(log_level)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

_LOGGER = logging.getLogger(__name__)


class DahuaVTOManager:
    def __init__(self):
        with open("version.json", "r") as file:
            version_data = json.load(file)
            version = version_data.get("version")

        _LOGGER.info(f"Starting DahuaVTO2MQTT, Version: {version}")

        self.registry = CollectorRegistry()

        self._mqtt_client = MQTTClient(version, self.registry)
        self._dahua_client = DahuaClient(version, self.registry)

        self.exporter_port = int(os.environ.get('EXPORTER_PORT', "9563"))

        self.version: str | None = None

    def initialize(self):
        start_http_server(self.exporter_port)

        self._mqtt_client.initialize(self._dahua_client.outgoing_events)
        self._dahua_client.initialize(self._mqtt_client.outgoing_events)

        while True:
            sleep(1)


manager = DahuaVTOManager()
manager.initialize()
