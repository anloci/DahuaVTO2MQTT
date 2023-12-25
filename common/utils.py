import hashlib
import json
import logging

from common.consts import JSON_START_PATTERN

_LOGGER = logging.getLogger(__name__)


def parse_data(data):
    _LOGGER.debug(f"Parsing data, Content: {data}")

    if not __is_dhip_message(data):
        raise Exception("The beginning of the stream does not start with a DHIP header")

    messages = []

    while len(data) > 0:
        if not __is_dhip_message(data):
            return messages, b''

        # Code taken from https://github.com/mcw0/PoC/blob/master/Dahua-DHIP-JSON-Debug-Console.pyhttps://github.com/mcw0/PoC/blob/master/Dahua-DHIP-JSON-Debug-Console.py
        header = data[0:32]
        _LOGGER.debug("\n-HEADER-  -DHIP-  SessionID   ID      LEN               LEN")
        _LOGGER.debug("{}|{}|{}|{}|{}|{}|{}|{}".format(
            header[0:4].hex(), header[4:8].hex(), header[8:12].hex(),
            header[12:16].hex(), header[16:20].hex(), header[20:24].hex(),
            header[24:28].hex(), header[28:32].hex()))
        data_length = int.from_bytes(header[16:24], "little")
        if data_length <= (len(data) - 32):
            json_data = data[32:data_length + 32]
            data = data[data_length + 32:]
            messages.append(json_data.decode("utf-8"))
        else:
            return messages, data
    return messages, data


def __is_dhip_message(stream):
    return stream[0:8] == b'\x20\x00\x00\x00\x44\x48\x49\x50'


def parse_message(message_data):
    result = None

    try:
        if message_data is not None and JSON_START_PATTERN in message_data:
            idx = message_data.index(JSON_START_PATTERN)
            message = message_data[idx:]

            if message is not None:
                result = json.loads(message)

    except Exception as e:
        error_message = (
            f"Failed to read data: {message_data}, "
            f"Error: {e}"
        )

        raise Exception(error_message)

    return result


def get_hashed_password(random, realm, username, password):
    password_str = f"{username}:{realm}:{password}"
    password_bytes = password_str.encode('utf-8')
    password_hash = hashlib.md5(password_bytes).hexdigest().upper()

    random_str = f"{username}:{random}:{password_hash}"
    random_bytes = random_str.encode('utf-8')
    random_hash = hashlib.md5(random_bytes).hexdigest().upper()

    return random_hash
