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

    b = b.hex().upper()

    return b
