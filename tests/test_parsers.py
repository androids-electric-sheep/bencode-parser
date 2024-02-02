import pytest

from bencode_parser import parsers


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param(
            b"i234eRANDOM", (234, b"RANDOM"), id="integer with following content"
        ),
        pytest.param(b"i456e", (456, b""), id="integer with no following content"),
    ],
)
def test_integer_parser(input_value, expected_output) -> None:
    assert parsers.parse_integer(input_value) == expected_output


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param(
            b"4:aaaa", (b"aaaa", b""), id="byte string with no following content"
        ),
        pytest.param(
            b"4:aaaai23e", (b"aaaa", b"i23e"), id="byte string with following content"
        ),
    ],
)
def test_byte_string_parser(input_value, expected_output) -> None:
    assert parsers.parse_byte_string(input_value) == expected_output


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param(
            b"i234e4:aaaa", [234, b"aaaa"], id="integer followed by byte string"
        ),
    ],
)
def test_parse(input_value, expected_output) -> None:
    assert parsers.parse(input_value) == expected_output
