from bencode_parser import decoders, encoders


def test_decode_then_encode(torrent_file) -> None:
    """
    Test that decoding a file and then re-encoding it
    is essentially a nop
    """
    with open(torrent_file, "rb") as in_fh:
        data = in_fh.read()
    output_value = encoders.encode(decoders.decode(data)[0])
    assert output_value == data
