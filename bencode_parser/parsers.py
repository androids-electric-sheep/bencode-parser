import re


def parse_integer(value: bytes) -> tuple[int, bytes]:
    if value[0] != ord("i"):
        raise ValueError("Invalid input format")
    ending_delimiter = value.find(b"e")
    integer_value = int(value[1:ending_delimiter])
    remaining_value = value[ending_delimiter + 1 :]
    return integer_value, remaining_value


def parse_byte_string(value: bytes) -> tuple[bytes, bytes]:
    if not re.match(b"^[0-9]+:.+", value):
        raise ValueError("Invalid input format")
    raise NotImplementedError("blah")
