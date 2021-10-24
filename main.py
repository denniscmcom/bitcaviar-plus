import os
from puppy.block import deserialize_block


def main():
    filename = '/Users/dennis/Bitcoin/blocks/blk00000.dat'
    file_size = os.path.getsize(filename)
    print('File size in bytes: {}'. format(file_size))

    with open(filename, 'rb') as f:
        while f.tell() < file_size:
            block = deserialize_block(f)


if __name__ == '__main__':
    main()
