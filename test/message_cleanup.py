#!/usr/bin/env python3
import os
import sys
import logging

import clients.DahuaAPI as DahuaAPI
from common.utils import parse_message, parse_data

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


data_items = [
    
]


for data in data_items:
    messages = parse_data(data)
    print(f"Original: {messages}")

    for message_data in messages:
        message = parse_message(message_data.lstrip(), data)

        print(message)

