def read_bytes(file, number_of_bytes, bytes_order='backward'):
    """
    Read bytes from buffer
    :param file: <class '_io.BufferedReader'>, required
    :param number_of_bytes: int, required
    :param bytes_order: string, 'backward' or 'forward', required
    :return: string
    """

    # More info about bytes order: https://en.wikipedia.org/wiki/Endianness

    b = file.read(number_of_bytes)
    if bytes_order == 'backward':
        b = b[::-1]

    return b


def get_variable_int(file):
    """
    Get variable int from transaction data
    More info: https://learnmeabitcoin.com/technical/varint
    :param file: <class '_io.BufferedReader'>, required
    :return: int
    """

    first_byte = read_bytes(file, 1)

    if first_byte == b'\xfd':
        variable_int_bytes = read_bytes(file, 2)
    elif first_byte == b'\xfe':
        variable_int_bytes = read_bytes(file, 4)
    elif first_byte == b'\xff':
        variable_int_bytes = read_bytes(file, 8)
    else:
        variable_int_bytes = first_byte

    return int.from_bytes(variable_int_bytes, 'little')
