import hashlib


def __get_hash(buffer, bytes_order='backward'):
    """
    Compute hash from bytes
    More info about bytes order: https://en.wikipedia.org/wiki/Endianness
    :param buffer: bytes, required
    :param bytes_order: string, 'backward' or 'forward', optional
    :return: string
    """

    h = hashlib.sha256(buffer).digest()
    h = hashlib.sha256(h).digest()

    if bytes_order == 'backward':
        h = h[::-1]

    return h.hex()


def __get_variable_int(f):
    """
    Get variable int from transaction data
    More info: https://learnmeabitcoin.com/technical/varint
    :param f: buffer, required
    :return: int
    """

    first_byte = f.read(1)

    if first_byte == b'\xfd':
        variable_int_bytes = f.read(2)[::-1]
    elif first_byte == b'\xfe':
        variable_int_bytes = f.read(4)[::-1]
    elif first_byte == b'\xff':
        variable_int_bytes = f.read(8)[::-1]
    else:
        variable_int_bytes = first_byte

    return int.from_bytes(variable_int_bytes, 'little')