# Token Swap Transaction Builder

This script builds and sends a token swap transaction using the `BuildTokenSwapTX` class.

## Prerequisites

- Python 3.x
- `python-dotenv` package
- `ergpy` package
- Create a .env file in the root directory of the project to store your wallet addresses. Add the following lines to the .env file:
    - `SWAP_MNEMONIC = 'Your_SEED_PHRASE'`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/marctheshark3/ergo-tx-factory
   cd ergo-tx-factory
   ```

2. pip install -r requirements.txt

## Usage

### Using the CLI

Run the script from the command line with the required arguments:

```bash
python token_swap.py --my_wallet <my_wallet_address> --miner_wallet <miner_wallet_address>
```

This command returns None if there is not miner ID otherwise it will return the miners minimum payout
```bash
python confirm_miner_ID.py --miner_wallet <miner_wallet_address>
```

