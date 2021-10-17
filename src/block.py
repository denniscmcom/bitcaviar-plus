import hashlib
from src.helpers import read_bytes
from src.helpers import get_variable_int


class Block:
    """
    Block structure
    """

    block_hash = str()
    magic_number = int()
    size = int()
    number_of_transactions = int()
    transactions = []

    class Header:
        version = int()
        previous_block_hash = str()
        merkle_root = str()
        timestamp = int()  # Epoch Unix time
        difficult_target = int()  # Bits
        nonce = int()


class Transaction:
    id = str()
    version = int()
    number_of_inputs = int()
    inputs = []

    class Inputs:
        pass


def read_block(file):
    """
    Deserialize block
    More info about block structure: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch09.asciidoc
    :param file: <class '_io.BufferedReader'>, required
    :return:
    """

    block = Block()
    block.magic_number = int.from_bytes(read_bytes(file, 4), 'big')
    block.size = int.from_bytes(read_bytes(file, 4), 'big')

    # Compute block hash
    header_bytes = read_bytes(file, 80, 'forward')
    block_hash = hashlib.sha256(header_bytes).digest()
    block_hash = hashlib.sha256(block_hash).digest()

    # Read block header
    header = block.Header()
    header.block_hash = block_hash[::-1].hex()
    header.version = int.from_bytes(header_bytes[:4], 'little')
    header.previous_block_hash = header_bytes[4:36][::-1].hex()
    header.merkle_root = header_bytes[36:68][::-1].hex()
    header.timestamp = int.from_bytes(header_bytes[68:72], 'little')
    header.difficult_target = int.from_bytes(header_bytes[72:76], 'little')
    header.nonce = int.from_bytes(header_bytes[76:80], 'little')

    # Number of transactions (varInt)
    block.number_of_transactions = get_variable_int(file)

    # Compute transaction ID
    # Get remaining bytes until the end of the block
    transaction = Transaction()
    bytes_read = file.tell()
    whole_block_size = block.size + 8  # Plus magic number and block size
    transaction_data_size = whole_block_size - bytes_read
    transaction_data = file.read(transaction_data_size)
    file.seek(bytes_read)  # Set position to where 'transaction data' starts
    transaction_id = hashlib.sha256(transaction_data).digest()
    transaction_id = hashlib.sha256(transaction_id).digest()
    transaction.id = transaction_id[::-1].hex()

    transaction.version = int.from_bytes(read_bytes(file, 4), 'little')
    transaction.number_of_inputs = get_variable_int(file)



