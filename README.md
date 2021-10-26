# bitcaviar-plus
A Bitcoin blockchain parser written in Python.

## Installation
Clone repository
```bash
pip install bitcaviar-plus
```

## Usage
### Deserialize first block from file `blk00000.dat`
```python
from bitcaviar_plus.block import deserialize_block


def parse_genesis_block():
    with open('path/to/file/blk00000.dat', 'rb') as f:
        block = deserialize_block(f)
        print(block)
```

### Deserialize entire blockchain
```python
import os
from bitcaviar_plus.block import deserialize_block


def parse_entire_blockchain():
    file_counter = -1
    while True:
        file_counter += 1
        file_name = 'path/to/file/blk{}.dat'.format(str(file_counter).zfill(5))
        with open(file_name, 'rb') as f:
            file_size = os.path.getsize(file_name)
            while f.tell() < file_size:
                block = deserialize_block(f)
```

### Example output
```json
{
  "magic_number":"f9beb4d9",
  "size":"0000011d",
  "id":"000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
  "transaction_count":"01",
  "header":{
    "version":"00000001",
    "previous_block_id":"0000000000000000000000000000000000000000000000000000000000000000",
    "merkle_root":"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "time":"495fab29",
    "bits":"1d00ffff",
    "nonce":"7c2bac1d"
  },
  "transactions":[
    {
      "version":"00000001",
      "input_count":"01",
      "output_count":"01",
      "lock_time":"00000000",
      "id":"4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "inputs":[
        {
          "id":"0000000000000000000000000000000000000000000000000000000000000000",
          "vout":"ffffffff",
          "script_sig_size":"4d",
          "script_sig":"04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
          "sequence":"ffffffff"
        }
      ],
      "outputs":[
        {
          "value":"000000012a05f200",
          "script_pub_key_size":"43",
          "script_pub_key":"4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
        }
      ]
    }
  ]
}
```

## Attribution
- [blockchain-parser](https://github.com/ragestack/blockchain-parser/blob/master/blockchain-parser.py)
- [bitcoinbook](https://github.com/bitcoinbook/bitcoinbook)
- [LearnMeABitcoin.com](https://learnmeabitcoin.com)