import hashlib

"""
Helper methods
"""


def __get_var_int(f):
    """
    A VarInt (variable integer) is a field used in transaction data to indicate the number of upcoming fields,
    or the length of an upcoming field.
    More info: https://learnmeabitcoin.com/technical/varint
    :param f: buffer, required
    :return: string
    """

    prefix = f.read(1).hex()

    if int(prefix, 16) == 253:
        number_of_transactions = f.read(2)[::-1].hex()
    elif int(prefix, 16) == 254:
        number_of_transactions = f.read(4)[::-1].hex()
    elif int(prefix, 16) == 255:
        number_of_transactions = f.read(8)[::-1].hex()
    else:
        number_of_transactions = prefix

    return number_of_transactions


def __compute_hash(data):
    """
    Get hash
    :param data: bytes, required
    :return: string
    """

    h = hashlib.sha256(data).digest()
    h = hashlib.sha256(h).digest()

    return h[::-1].hex()
