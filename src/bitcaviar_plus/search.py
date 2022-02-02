"""
Search methods for LEVELDB database
"""

try:
    # noinspection PyUnresolvedReferences
    import plyvel
except ImportError:
    # Avoid import error running unit tests
    print("Couldn't import plyvel package. Are you running unit tests?")

import tempfile


def search_block_with(block_hash):
    """
    Search block with a given hash and get value
    :param block_hash: string, required
    :return: string
    """

    db = level_db_connect()
    search_type = bytes.fromhex('62')  # 'b' (block) in hex is 62
    block_hash = bytes.fromhex(block_hash)[::-1]
    key = search_type + block_hash
    value = db.get(key)
    db.close()

    return value.hex()


# ---- SECONDARY METHODS ----

def deserialize_block_search(f):
    """
    Deserialize value (block search)
    More info: https://bitcoin.stackexchange.com/questions/67515/format-of-a-block-keys-contents-in-bitcoinds-leveldb
    :param f: buffer, required
    :return: dict
    """

    client_number = f.read(3)
    print('Client number: {}'.format(client_number.hex()))
    block_height = f.read(1)  # Var int 128?
    print('Block height: {}'.format(block_height.hex()))
    status = f.read(1)  # var int 128?
    print('Status: {}'.format(status.hex()))
    number_of_transactions = f.read(1)  # var int 128?
    print('Number of transactions: {}'.format(number_of_transactions.hex()))


def create_file_with(binary):
    with tempfile.TemporaryFile() as fp:
        fp.write(binary)
        fp.seek(0)

    return fp


# noinspection PyUnresolvedReferences
def level_db_connect():
    db = plyvel.DB('/bitcoin-node/.bitcoin/blocks/index/', create_if_missing=False)

    return db


def get_128_var_int(f):
    """
    This var int is different from helpers.get_var_int
    :param f:
    :return: string
    """

    pass
