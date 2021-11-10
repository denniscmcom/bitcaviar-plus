import os
from bitcaviar_plus.block import deserialize_block
from bitcaviar_plus.errors import InvalidMagicBytes


def parse_genesis_block():
    blk_path = '/bitcoin-node/.bitcoin/blocks/blk00355.dat'

    with open(blk_path, 'rb') as f:
        file_size = os.path.getsize(blk_path)
        while f.tell() < file_size:
            try:
                block = deserialize_block(f)
            except InvalidMagicBytes as e:
                print(e)


if __name__ == '__main__':
    parse_genesis_block()
