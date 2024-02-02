import re
from typing import Any, Callable


def decode(encoded_string: bytes) -> list[Any]:
    pieces = []
    while encoded_string:
        decoder = identify_decoder(encoded_string)
        piece, encoded_string = decoder(encoded_string)
        pieces.append(piece)
    return pieces


def identify_decoder(encoded_string: bytes) -> Callable[[bytes], tuple[Any, bytes]]:
    if encoded_string[0] == ord("i"):
        return decode_integer
    elif encoded_string[0] == ord("d"):
        return decode_dictionary
    elif encoded_string[0] == ord("l"):
        return decode_list
    else:
        return decode_byte_string


def decode_integer(encoded_string: bytes) -> tuple[int, bytes]:
    if encoded_string[0] != ord("i"):
        raise ValueError("Invalid input format")
    ending_delimiter = encoded_string.find(b"e")
    integer_encoded_string = int(encoded_string[1:ending_delimiter])
    remaining_encoded_string = encoded_string[ending_delimiter + 1 :]
    return integer_encoded_string, remaining_encoded_string


def decode_byte_string(encoded_string: bytes) -> tuple[bytes, bytes]:
    content_length_match = re.match(b"^([0-9]+):.+", encoded_string)
    if not content_length_match:
        raise ValueError("Invalid input format")
    content_length = int(content_length_match.group(1))
    starting_point = len(str(content_length)) + 1
    return (
        encoded_string[starting_point : starting_point + content_length],
        encoded_string[starting_point + content_length :],
    )


def decode_list(encoded_string: bytes) -> tuple[list[Any], bytes]:
    if encoded_string[0] != ord("l"):
        raise ValueError("Invalid input format")
    encoded_string = encoded_string[1:]  # Strip off the 'l' prefix
    list_contents = []
    while encoded_string[0] != ord("e"):
        decoder = identify_decoder(encoded_string)
        list_entry, encoded_string = decoder(encoded_string)
        list_contents.append(list_entry)
    # Return the parsed list and strip the 'e' suffix off the remaining data
    return list_contents, encoded_string[1:]


def decode_dictionary(encoded_string: bytes) -> tuple[dict[Any, Any], bytes]:
    if encoded_string[0] != ord("d"):
        raise ValueError("Invalid input format")
    encoded_string = encoded_string[1:]  # Strip off the 'd' prefix
    dictionary_contents = {}
    while encoded_string[0] != ord("e"):
        key_parser = identify_decoder(encoded_string)
        key, encoded_string = key_parser(encoded_string)
        value_parser = identify_decoder(encoded_string)
        value, encoded_string = value_parser(encoded_string)
        dictionary_contents[key] = value
    # Return the parsed list and strip the 'e' prefix off the remaining data
    return dictionary_contents, encoded_string[1:]
