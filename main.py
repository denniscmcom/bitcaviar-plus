from src.block import read_block


def main():
    with open('/Users/dennis/Bitcoin/blocks/blk00000.dat', 'rb') as f:
        block = read_block(f)

        import json
        with open('test_block_0.json', 'w') as f_test:
            json.dump(block, f_test, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
