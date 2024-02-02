from typing import Any, Callable


def encode(obj: Any) -> bytes:
    encoder = identify_encoder(obj)
    encoded_string = encoder(obj)
    return encoded_string


def identify_encoder(obj: Any) -> Callable[[Any], bytes]:
    if isinstance(obj, list):
        return encode_list
    elif isinstance(obj, dict):
        return encode_dictionary
    elif isinstance(obj, int):
        return encode_integer
    elif isinstance(obj, (str, bytes)):
        return encode_byte_string
    raise ValueError(f"No encoder available for object type {type(obj)}")


def encode_integer(obj: int) -> bytes:
    return f"i{obj}e".encode("utf-8")


def encode_byte_string(obj: str | bytes) -> bytes:
    obj_len = len(obj)
    prefix_string = f"{obj_len}:".encode("utf-8")
    if isinstance(obj, str):
        obj = obj.encode("utf-8")
    return prefix_string + obj


def encode_list(obj: list[Any]) -> bytes:
    encoded_string = b"l"
    for entry in obj:
        encoded_string += encode(entry)
    encoded_string += b"e"
    return encoded_string


def encode_dictionary(obj: dict[Any, Any]) -> bytes:
    encoded_string = b"d"
    for key, value in obj.items():
        encoded_string += encode(key)
        encoded_string += encode(value)
    encoded_string += b"e"
    return encoded_string
