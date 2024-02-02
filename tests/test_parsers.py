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
            b"d3:bar4:spam3:fooi42ee",
            ({b"bar": b"spam", b"foo": 42}, b""),
            id="wikipedia example input",
        )
    ],
)
def test_parse_dictionary(input_value, expected_output) -> None:
    assert parsers.parse_dictionary(input_value) == expected_output


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param(
            b"i234e4:aaaa", [234, b"aaaa"], id="integer followed by byte string"
        ),
        pytest.param(
            b"l4:spami42eei123e", [[b"spam", 42], 123], id="list and an integer"
        ),
    ],
)
def test_parse(input_value, expected_output) -> None:
    assert parsers.parse(input_value) == expected_output


def test_parse_with_input_file(data_directory) -> None:
    target_filename = data_directory / "bbb_sunflower_1080p_60fps_normal.mp4.torrent"
    assert target_filename.is_file(), "Input file does not exist"
    with open(target_filename, "rb") as in_fh:
        data = in_fh.read()
    parsed_input = parsers.parse(data)
    assert len(parsed_input) == 1 and isinstance(parsed_input[0], dict)
    assert len(parsed_input[0]) == 9
