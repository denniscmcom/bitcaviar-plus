from src.helpers import __get_hash
from src.helpers import __get_variable_int
from src.block_structure import *


def read_block(f):
    """
    Deserialize block
    More info about block structure: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch09.asciidoc
    More info about bytes order: https://en.wikipedia.org/wiki/Endianness
    :param f: buffer, required
    :return:
    """

    block = Block()
    _ = f.read(4)  # Magic number
    _ = f.read(4)[::-1]  # Block size
    header_bytes = f.read(80)
    block.block_hash = __get_hash(header_bytes)
    f.seek(8)
    block.header = __get_header(f)
    number_of_transactions = __get_variable_int(f)

    transactions = []
    for transaction_number in range(number_of_transactions):
        transactions.append(__get_transaction(f))

    block_dict = block.__dict__
    block_dict['transactions'] = transactions

    return block_dict


def __get_header(f):
    """
    Get block header
    :param f: buffer, required
    :return: dict
    """

    header = Header()
    header.version = int.from_bytes(f.read(4), 'little')
    header.previous_block_hash = f.read(32)[::-1].hex()
    header.merkle_root = f.read(32)[::-1].hex()
    header.timestamp = int.from_bytes(f.read(4), 'little')
    header.bits = int.from_bytes(f.read(4), 'little')
    header.nonce = int.from_bytes(f.read(4), 'little')

    return header.__dict__


def __get_transaction(f):
    """
    Get transaction
    :param f: buffer, required
    :return: dict
    """

    transaction_data_start = f.tell()

    transaction = Transaction()
    transaction.version = int.from_bytes(f.read(4)[::-1], 'big')
    number_of_inputs = __get_variable_int(f)

    inputs = []
    for input_number in range(number_of_inputs):
        inputs.append(__get_input(f))

    number_of_outputs = __get_variable_int(f)

    outputs = []
    for output_number in range(number_of_outputs):
        outputs.append(__get_outputs(f))

    transaction.lock_time = int.from_bytes(f.read(4)[::-1], 'little')

    transaction_dict = transaction.__dict__
    transaction_dict['inputs'] = inputs
    transaction_dict['outputs'] = outputs

    transaction_data_end = f.tell()

    # Get transaction id
    transaction_data_size = transaction_data_end - transaction_data_start
    f.seek(transaction_data_start)
    transaction_data = f.read(transaction_data_size)
    transaction.id = __get_hash(transaction_data)

    return transaction_dict


def __get_input(buffer):
    """
    Get input from transaction data
    :param buffer: bytes, required
    :return: dict
    """

    transaction_input = TransactionInput()
    transaction_input.id = buffer.read(32)[::-1].hex()

    if transaction_input.id == '0000000000000000000000000000000000000000000000000000000000000000':
        transaction_input.is_coinbase = True

    transaction_input.vout = int.from_bytes(buffer.read(4)[::-1], 'little')
    script_sig_size = __get_variable_int(buffer)
    transaction_input.script_sig = buffer.read(script_sig_size).hex()
    transaction_input.sequence = int.from_bytes(buffer.read(4)[::-1], 'little')

    return transaction_input.__dict__


def __get_outputs(buffer):
    """
    Get output from transaction data
    :param buffer: bytes, required
    :return: dict
    """

    transaction_output = TransactionOutput()
    transaction_output.value = float.fromhex(buffer.read(8)[::-1].hex())
    transaction_output.value /= 100000000  # Satoshis to BTC
    script_pub_key_size = __get_variable_int(buffer)
    transaction_output.script_pub_key = buffer.read(script_pub_key_size).hex()

    return transaction_output.__dict__
