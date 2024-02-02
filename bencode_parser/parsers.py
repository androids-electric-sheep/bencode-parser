import re


def parse_integer(value: bytes) -> tuple[int, bytes]:
    if value[0] != ord("i"):
        raise ValueError("Invalid input format")
    ending_delimiter = value.find(b"e")
    integer_value = int(value[1:ending_delimiter])
    remaining_value = value[ending_delimiter + 1 :]
    return integer_value, remaining_value


def parse_byte_string(value: bytes) -> tuple[bytes, bytes]:
    content_length_match = re.match(b"^([0-9]+):.+", value)
    if not content_length_match:
        raise ValueError("Invalid input format")
    content_length = int(content_length_match.group(1))
    starting_point = len(str(content_length)) + 1
    return (
        value[starting_point : starting_point + content_length],
        value[starting_point + content_length :],
    )
