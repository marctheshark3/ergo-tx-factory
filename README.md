# Sigmanauts Mining Core - Payment Mechanism
This code base performs the needed execute of payments to miners when balances are over the minimum payout threshold. Additionally, this code supports the swapping of native tokens from the pool's wallet to the miners wallet based on spectrum prices as well as looking for changes in minimum payouts. 

One can look at the token swap as "a dollar cost averaging" approach into Ergo's Native Tokens of choice. 


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

TBD

