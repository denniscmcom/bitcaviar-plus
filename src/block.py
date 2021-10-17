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
    number_of_outputs = int()
    outputs = []

    class TransactionInput:
        id = str()
        is_coinbase = False
        vout = int()
        script_sig_size = int()
        script_sig = str()
        sequence = int()

    class TransactionOutput:
        value = float()
        script_pub_key_size = int()
        script_pub_key = str()


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

    for transaction_number in range(block.number_of_transactions):
        transaction = Transaction()
        transaction.version = int.from_bytes(read_bytes(file, 4), 'big')
        transaction.number_of_inputs = get_variable_int(file)

        for input_number in range(transaction.number_of_inputs):
            transaction_input = transaction.TransactionInput()
            transaction_input.id = read_bytes(file, 32).hex()
            if transaction_input.id == '0000000000000000000000000000000000000000000000000000000000000000':
                transaction_input.is_coinbase = True

            transaction_input.vout = int.from_bytes(read_bytes(file, 4), 'little')
            transaction_input.script_sig_size = get_variable_int(file)
            transaction_input.script_sig = read_bytes(file, transaction_input.script_sig_size, 'forward').hex()
            transaction_input.sequence = int.from_bytes(read_bytes(file, 4), 'little')

        transaction.number_of_outputs = get_variable_int(file)

        for output_number in range(transaction.number_of_outputs):
            transaction_output = transaction.TransactionOutput()
            transaction_output.value = float.fromhex(read_bytes(file, 8).hex())
            transaction_output.value /= 100000000  # Satoshis to BTC
