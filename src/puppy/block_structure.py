class Block:
    block_hash = str()
    magic_number = str()
    block_size = str()
    number_of_transactions = str()


class Header:
    version = str()
    previous_block_hash = str()
    merkle_root = str()
    time = str()
    bits = str()
    nonce = str()


class Transaction:
    id = str()
    version = str()
    number_of_inputs = str()
    number_of_outputs = str()
    lock_time = str()


class TransactionInput:
    id = str()
    vout = str()
    script_sig_size = str()
    script_sig = str()
    sequence = str()


class TransactionOutput:
    value = str()
    script_pub_key_size = str()
    script_pub_key = str()
