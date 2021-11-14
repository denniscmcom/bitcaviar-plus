import os
import plyvel
import tempfile
from bitcaviar_plus.block import deserialize_block
from bitcaviar_plus.block import __deserialize_header
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


# noinspection PyUnresolvedReferences
def iterate_leveldb_keys():
    db = plyvel.DB('/bitcoin-node/.bitcoin/blocks/index/', create_if_missing=False)
    for key, value in db:
        print('---- RAW KEY ----')
        print(key.hex())
        print('---- LITTLE ENDIAN KEY ----')
        print(key[::-1].hex())
        print('---- RAW VALUE ----')
        print(value[::-1].hex())
        exit()


# noinspection PyUnresolvedReferences
def search_block():
    db = plyvel.DB('/bitcoin-node/.bitcoin/blocks/index/', create_if_missing=False)
    search_type = bytes.fromhex('62')  # 'b' (block) in hex is 62
    block_hash = bytes.fromhex('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')[::-1]
    key = search_type + block_hash
    value = db.get(key)
    print(value.hex())
    db.close()


if __name__ == '__main__':
    search_block()
