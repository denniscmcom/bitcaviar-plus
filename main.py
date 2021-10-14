from src.block import read_block


def main():
    with open('/Users/dennis/Bitcoin/blocks/blk00000.dat', 'rb') as file:
        read_block(file)


if __name__ == '__main__':
    main()
