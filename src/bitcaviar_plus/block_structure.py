class Block:
    id = str()
    magic_number = str()
    size = str()
    transaction_count = str()


class Header:
    version = str()
    previous_block_id = str()
    merkle_root = str()
    time = str()
    bits = str()
    nonce = str()


class Transaction:
    id = str()
    version = str()
    input_count = str()
    output_count = str()
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
