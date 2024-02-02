def parse_integer(value: str) -> tuple[int, str]:
    if value[0] != "i":
        raise ValueError("Invalid input format")
    ending_delimiter = value.find("e")
    integer_value = int(value[1:ending_delimiter])
    remaining_value = value[ending_delimiter + 1 :]
    return integer_value, remaining_value
