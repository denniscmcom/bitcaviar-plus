import hashlib
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
    block.h = __get_hash(header_bytes)
    f.seek(8)
    block.header = __get_header(f)
    number_of_transactions = __get_variable_int(f)
    for transaction_number in range(number_of_transactions):
        block.transactions.append(__get_transaction(f))

    return block.__dict__


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

    transaction = Transaction()
    transaction.version = int.from_bytes(f.read(4)[::-1], 'big')
    number_of_inputs = __get_variable_int(f)

    for input_number in range(number_of_inputs):
        transaction_input = TransactionInput()
        transaction_input.id = f.read(32)[::-1].hex()

        if transaction_input.id == '0000000000000000000000000000000000000000000000000000000000000000':
            transaction_input.is_coinbase = True

        transaction_input.vout = int.from_bytes(f.read(4)[::-1], 'little')
        script_sig_size = __get_variable_int(f)
        transaction_input.script_sig = f.read(script_sig_size).hex()
        transaction_input.sequence = int.from_bytes(f.read(4)[::-1], 'little')
        transaction.inputs.append(transaction_input.__dict__)

    number_of_outputs = __get_variable_int(f)

    for output_number in range(number_of_outputs):
        transaction_output = TransactionOutput()
        transaction_output.value = float.fromhex(f.read(8)[::-1].hex())
        transaction_output.value /= 100000000  # Satoshis to BTC
        script_pub_key_size = __get_variable_int(f)
        transaction_output.script_pub_key = f.read(script_pub_key_size)
        transaction.outputs.append(transaction_output.__dict__)

    transaction.lock_time = int.from_bytes(f.read(4)[::-1], 'little')

    print(transaction.outputs)
    print(transaction.inputs)
    print(transaction.__dict__)

    return transaction.__dict__


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
