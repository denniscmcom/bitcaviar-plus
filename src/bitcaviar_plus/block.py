from bitcaviar_plus.block_structure import *
from bitcaviar_plus.helpers import __get_var_int
from bitcaviar_plus.helpers import __compute_hash

"""
Deserialize methods
"""


def deserialize_block(f):
    """
    Deserialize block
    :param f: buffer, required
    :return: dict
    """

    block = Block()
    block.magic_number = f.read(4).hex()
    block.size = f.read(4)[::-1].hex()
    block_header, block.id = __deserialize_header(f)
    block.transaction_count = __get_var_int(f)

    transactions = []
    for transaction_number in range(int(block.transaction_count, 16)):
        transactions.append(__deserialize_transaction_data(f))

    block_dict = block.__dict__
    block_dict['header'] = block_header
    block_dict['transactions'] = transactions

    return block_dict


def __deserialize_header(f):
    """
    Deserialize block header
    More info: https://learnmeabitcoin.com/technical/block-header
    :param f: buffer, required
    :return: (dict, string)
    """

    # Compute block hash
    before = f.tell()
    header = f.read(80)
    block_hash = __compute_hash(header)
    f.seek(before)

    header = Header()
    header.version = f.read(4)[::-1].hex()
    header.previous_block_id = f.read(32)[::-1].hex()
    header.merkle_root = f.read(32)[::-1].hex()
    header.time = f.read(4)[::-1].hex()
    header.bits = f.read(4)[::-1].hex()
    header.nonce = f.read(4)[::-1].hex()

    return header.__dict__, block_hash


def __deserialize_transaction_data(f):
    """
    Deserialize transaction data
    More info: https://learnmeabitcoin.com/technical/transaction-data
    :param f: buffer, required
    :return: dict
    """

    transaction = Transaction()
    start_transaction_data = f.tell()
    transaction.version = f.read(4)[::-1].hex()
    transaction.input_count = __get_var_int(f)

    transaction_inputs = []
    for input_number in range(int(transaction.input_count, 16)):
        transaction_input = TransactionInput()
        transaction_input.id = f.read(32)[::-1].hex()
        transaction_input.vout = f.read(4)[::-1].hex()
        transaction_input.script_sig_size = __get_var_int(f)
        transaction_input.script_sig = f.read(int(transaction_input.script_sig_size, 16)).hex()
        transaction_input.sequence = f.read(4)[::-1].hex()
        transaction_inputs.append(transaction_input.__dict__)

    transaction.output_count = __get_var_int(f)

    transaction_outputs = []
    for output_number in range(int(transaction.output_count, 16)):
        transaction_output = TransactionOutput()
        transaction_output.value = f.read(8)[::-1].hex()
        transaction_output.script_pub_key_size = __get_var_int(f)
        transaction_output.script_pub_key = f.read(int(transaction_output.script_pub_key_size, 16)).hex()
        transaction_outputs.append(transaction_output.__dict__)

    transaction.lock_time = f.read(4)[::-1].hex()

    # Compute transaction id
    end_transaction_data = f.tell()
    transaction_data_size = end_transaction_data - start_transaction_data
    f.seek(start_transaction_data)
    transaction_data = f.read(transaction_data_size)
    f.seek(end_transaction_data)
    transaction.id = __compute_hash(transaction_data)

    transaction_dict = transaction.__dict__
    transaction_dict['inputs'] = transaction_inputs
    transaction_dict['outputs'] = transaction_outputs

    return transaction_dict
