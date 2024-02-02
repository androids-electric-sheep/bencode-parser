import pytest

from bencode_parser import encoders


def test_encode_integer() -> None:
    assert encoders.encode_integer(1234) == b"i1234e"


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param("testing", b"7:testing", id="basic string"),
        pytest.param(
            b"\x11\x12\xBFtest", b"7:\x11\x12\xBFtest", id="string with hex characters"
        ),
    ],
)
def test_encode_byte_string(input_value, expected_output) -> None:
    assert encoders.encode_byte_string(input_value) == expected_output


def test_encode_list() -> None:
    assert (
        encoders.encode([123, {"game": "bet"}, b"\x11\x12test", ["a", "b"]])
        == b"li123ed4:game3:bete6:\x11\x12testl1:a1:bee"
    )


def test_encode_dictionary() -> None:
    assert (
        encoders.encode({"testing": "another", 1: b"more"})
        == b"d7:testing7:anotheri1e4:moree"
    )


@pytest.mark.parametrize(
    ["input_value", "expected_output"],
    [
        pytest.param(123, b"i123e", id="integer"),
        pytest.param("another", b"7:another", id="string"),
        pytest.param(
            {b"a": [1, {"a": 10}]},
            b"d1:ali1ed1:ai10eeee",
            id="heterogeneous dictionary",
        ),
        pytest.param([1, b"another"], b"li1e7:anothere", id="list"),
    ],
)
def test_encode(input_value, expected_output) -> None:
    assert encoders.encode(input_value) == expected_output
