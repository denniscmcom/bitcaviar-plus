import os
from src.puppy.block import read_block


def main():
    file_path = '/Users/dennis/Bitcoin/blocks/blk00000.dat'

    with open(file_path, 'rb') as f:
        number_of_bytes_in_file = os.path.getsize(file_path)

        while f.tell() < number_of_bytes_in_file:
            block = read_block(f)


if __name__ == '__main__':
    main()
