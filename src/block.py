import hashlib
from src.helpers import read_bytes


class Block:
    """
    Block structure
    """

    block_hash = None
    magic_number = None
    size = None

    def __init__(self):
        # Init BlockHeader class
        self.header = self.Header()

    class Header:
        version = None
        previous_block_hash = None
        merkle_root = None
        timestamp = None
        difficult_target = None
        nonce = None


def read_block(file):
    """
    Deserialize block
    :param file: <class '_io.BufferedReader'>, required
    :return:
    """

    block = Block()
    block.magic_number = int(read_bytes(file, 4), 16)
    block.size = int(read_bytes(file, 4), 16)

    # Compute block hash
    header_bytes = file.read(80)
    block_hash = hashlib.sha256(header_bytes).digest()
    block_hash = hashlib.sha256(block_hash).digest()

    # Read block header
    header = block.Header()
    header.block_hash = block_hash[::-1].hex()
    header.version = int.from_bytes(header_bytes[:4], 'little')
    header.previous_block_hash = header_bytes[4:32].hex()

