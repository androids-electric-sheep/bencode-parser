import re
from typing import Any, Callable


def parse(value: bytes) -> list[Any]:
    pieces = []
    while value:
        parser = identify_parser(value)
        piece, value = parser(value)
        pieces.append(piece)
    return pieces


def identify_parser(value: bytes) -> Callable[[bytes], tuple[Any, bytes]]:
    if value[0] == ord("i"):
        return parse_integer
    elif value[0] == ord("d"):
        return parse_dictionary
    elif value[0] == ord("l"):
        return parse_list
    else:
        return parse_byte_string


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


def parse_list(value: bytes) -> tuple[list[Any], bytes]:
    value = value[1:]  # Strip off the 'l' prefix
    list_contents = []
    while value[0] != ord("e"):
        parser = identify_parser(value)
        list_entry, value = parser(value)
        list_contents.append(list_entry)
    # Return the parsed list and strip the 'e' suffix off the remaining data
    return list_contents, value[1:]


def parse_dictionary(value: bytes) -> tuple[dict[Any, Any], bytes]:
    value = value[1:]  # Strip off the 'd' prefix
    dictionary_contents = {}
    while value[0] != ord("e"):
        dictionary_key_parser = identify_parser(value)
        dictionary_key, value = dictionary_key_parser(value)
        dictionary_value_parser = identify_parser(value)
        dictionary_value, value = dictionary_value_parser(value)
        dictionary_contents[dictionary_key] = dictionary_value
    # Return the parsed list and strip the 'e' prefix off the remaining data
    return dictionary_contents, value[1:]
