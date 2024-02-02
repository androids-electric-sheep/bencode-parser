from bencode_parser import parsers


def test_integer_parser() -> None:
    test_value = "i234eRANDOM"
    assert parsers.parse_integer(test_value) == (234, "RANDOM")
