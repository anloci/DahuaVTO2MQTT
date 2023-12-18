import hashlib
import json
import re
import logging
import sys

from common.consts import *

_LOGGER = logging.getLogger(__name__)


def parse_data(data):
    _LOGGER.debug(f"Parsing data, Content: {data}")

    data_items = bytearray()

    for data_item in data:
        data_item_char = chr(data_item)
        parsed_char = ascii(data_item_char).replace("'", "")
        is_valid = data_item_char == parsed_char

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


def get_hashed_password(random, realm, username, password):
    password_str = f"{username}:{realm}:{password}"
    password_bytes = password_str.encode('utf-8')
    password_hash = hashlib.md5(password_bytes).hexdigest().upper()

    random_str = f"{username}:{random}:{password_hash}"
    random_bytes = random_str.encode('utf-8')
    random_hash = hashlib.md5(random_bytes).hexdigest().upper()

    return random_hash
