from unittest import TestCase
from testfixtures import TempDirectory
from bitcaviar_plus.block import deserialize_block
from bitcaviar_plus.search import deserialize_block_search


class TestBlockUnit(TestCase):
    """
    Test block.py file
    """

    genesis_block_hex = """
    f9beb4d91d0100000100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67
    768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000000000000000000000000
    000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72
    206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0
    fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6b
    f11d5fac00000000
    """

    def test_deserialize_header(self):
        pass

    def test_deserialize_transaction_data(self):
        pass


class TestHelpersUnit(TestCase):
    """
    Test helpers.py file
    """

    def test_get_var_int(self):
        pass

    def test_compute_hash(self):
        pass


class TestSearchUnit(TestCase):
    """
    Test search.py file
    """

    genesis_block_value = """
    8be834000b0100080100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67
    768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c
    """

    first_block_value = """
    8be834011d0100812d08010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe68
    0e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299
    """

    def test_deserialize_block_search(self):
        with TempDirectory() as d:
            genesis_block_search_binary = bytes.fromhex(self.genesis_block_value)
            d.write('test_block_search.dat', genesis_block_search_binary)

            with open('{}/test_block_search.dat'.format(d.path), 'rb') as f:
                deserialize_block_search(f)

    def test_create_file_with(self):
        pass
