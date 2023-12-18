#!/usr/bin/env python3
import json
import os
import sys
import logging
import re
from common.consts import MESSAGE_PREFIX_PATTERN

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


def parse_data(data):
    _LOGGER.debug(f"Parsing data, Content: {data}")

    data_items = bytearray()

    for data_item in data:
        data_item_char = chr(data_item)
        parsed_char = ascii(data_item_char).replace("'", "")
        is_valid = data_item_char == parsed_char or data_item_char in ['\n', '\'']

        if is_valid:
            data_items.append(data_item)

    messages = data_items.decode("unicode-escape").split("\n")

    _LOGGER.debug(f"Data cleaned up, Messages: {messages}")

    return messages


def parse_message(message_data, original_data):
    result = None

    try:
        if message_data is not None and len(message_data) > 0:
            message_parts = re.split(MESSAGE_PREFIX_PATTERN, message_data)
            message_parts_count = len(message_parts)
            message: str | None = None

            if message_parts_count == 1:
                message = message_parts[0]

            elif message_parts_count > 1:
                message = message_parts[message_parts_count - 1]

            if message is not None:
                result = json.loads(message)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        _LOGGER.error(
            f"Failed to read data: {message_data}, "
            f"Original Data: {original_data}, "
            f"Error: {e}, "
            f"Line: {exc_tb.tb_lineno}"
        )

    return result



data = b' \x00\x00\x00DHIPb\xfe\xff\x7f\x02\x00\x00\x00 \x01\x00\x00\x00\x00\x00\x00 \x01\x00\x00\x00\x00\x00\x00{"error":{"code":268632079,"message":"Component error: login challenge!"},"id":2,"params":{"authorization":"fe2eaba1625968a96cadd6cd5bb3367185d47539","encryption":"Default","mac":"BC325FAF5332","random":"647709486","realm":"Login to 6J0DA6EPAJ4FE11"},"result":false,"session":2147483234}\n'

messages = parse_data(data)
print(messages)

for message_data in messages:
    message = parse_message(message_data.lstrip(), data)

    print(message)

