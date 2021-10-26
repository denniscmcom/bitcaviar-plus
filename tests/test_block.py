from unittest import TestCase
from testfixtures import TempDirectory
from bitcaviar_plus.block import deserialize_block


class TestBlock(TestCase):
    genesis_block_hex = """
    f9beb4d91d0100000100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67
    768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000000000000000000000000
    000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72
    206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0
    fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6b
    f11d5fac00000000
    """

    expected_genesis_block = {
        'magic_number': 'f9beb4d9',
        'size': '0000011d',
        'id': '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        'transaction_count': '01',
        'header': {
            'version': '00000001',
            'previous_block_id': '0000000000000000000000000000000000000000000000000000000000000000',
            'merkle_root': '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
            'time': '495fab29',
            'bits': '1d00ffff',
            'nonce': '7c2bac1d'
        },
        'transactions': [{
            'version': '00000001',
            'input_count': '01',
            'output_count': '01',
            'lock_time': '00000000',
            'id': '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
            'inputs': [{
                'id': '0000000000000000000000000000000000000000000000000000000000000000',
                'vout': 'ffffffff',
                'script_sig_size': '4d',
                'script_sig': '04ffff001d0104455468652054696d65732030332f4a616e'
                              '2f32303039204368616e63656c6c6f72206f6e206272696e'
                              '6b206f66207365636f6e64206261696c6f757420666f722062616e6b73',
                'sequence': 'ffffffff'
            }],
            'outputs': [{
                'value': '000000012a05f200',
                'script_pub_key_size': '43',
                'script_pub_key': '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f'
                                  '6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac'
            }]
        }]
    }

    def test_deserialize_block(self):
        with TempDirectory() as d:
            test_block_binary = bytes.fromhex(self.genesis_block_hex)
            d.write('test_block.dat', test_block_binary)

            with open('{}/test_block.dat'.format(d.path), 'rb') as f:
                block = deserialize_block(f)
                self.assertEqual(
                    block, self.expected_genesis_block, 'Genesis block is not equal to expected genesis block'
                )
