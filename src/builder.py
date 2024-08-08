from contextlib import redirect_stdout
from ergpy import appkit
from ergpy import helper_functions
from src.converter import ConvertTokens
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import time

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='sigs_core.log')

class BuildTokenSwapTX:
    def __init__(self):
        self.converter = ConvertTokens()
        load_dotenv()
        self.seed_phrase = os.getenv('SWAP_MNEMONIC')
        self.miner_fee = 0.0012
        self.logger = logging.getLogger(__name__)

    def get_api_data(self, api_url):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                self.logger.error(f"Failed to retrieve data: Status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred during API request: {e}")
            return None

    def get_token_data(self, miner_wallet, payout):
        self.logger.info(f"Getting token data for miner wallet: {miner_wallet}, payout: {payout}")
        df = pd.read_csv('https://raw.githubusercontent.com/marctheshark3/Mining-Reward-Tokens/main/supported-tokens.csv')
        results = self.converter.execute(miner_wallet, payout)

        token_data = []
        ergo_data = []
        for key in results.keys():
            value = results[key]
            temp_df = df[df['Token Name'] == key]
            data = {'tokenId': temp_df['Token ID'].values[0], 'amount': value, 'token': key}
            if key == 'ERGO':
                ergo_data = data
                continue
            token_data.append(data)
        self.logger.info(f"Token data retrieved: {token_data}, Ergo data: {ergo_data}")
        return token_data, ergo_data, results

    def wait_for_tx_to_clear(self, tx):
        self.logger.info(f"Waiting for transaction to clear: {tx}")
        api = 'https://api.ergoplatform.com/api/v1/transactions'
        tx_api = f'{api}/{tx}'
        while True:
            self.logger.info(f'Checking for confirmation of tx: {tx}')
            try:
                tx_data = self.get_api_data(tx_api)
                status = tx_data['id']
                self.logger.info('TX CONFIRMED')
                break
            except Exception:
                self.logger.warning('TX UNconfirmed......Going to Sleep!')
                time.sleep(120)

    def check_for_current_txs(self):
        self.logger.info("Checking for current transactions")
        while True:
            api = 'https://api.ergoplatform.com/api/v1/mempool/transactions/byAddress'
            tx_api = f'{api}/{self.pool_address}'
            data = self.get_api_data(tx_api)
            if data.items:
                continue
            else:
                break
        self.logger.info("No current transactions found")

    def send_erg(self, ergo, rx, amount):
        self.logger.info(f"Sending ERG: {amount} to {rx}")
        receiver_addresses = [rx]
        amount = [amount]
        try:
            tx = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=self.seed_phrase,
                                              receiver_addresses=receiver_addresses, fee=self.miner_fee)
            self.logger.info(f"ERG sent successfully. TX: {tx}")
        except Exception as e:
            self.logger.error(f"Error sending ERG: {e}")
            tx = 'NOT ENOUGH LIQUIDITY'
        return tx

    def send_tokens(self, ergo, ergo_data, token_data, rx):
        self.logger.info(f"Sending tokens to {rx}")
        tokens = [[token['tokenId']] for token in token_data]
        amount_tokens = [[token['amount']] for token in token_data]
        receiver_addresses = [rx for _ in range(len(tokens))]

        if ergo_data:
            self.logger.info("Sending ERG along with tokens")
            amount = [ergo_data['amount'] / len(tokens) for _ in range(len(tokens))]
        else:
            self.logger.info("Sending minimum ERG amount with tokens")
            amount = [0.0001 for _ in range(len(tokens))]
        
        self.logger.info(f"Token data: {tokens}, Amount tokens: {amount_tokens}, ERG amount: {amount}")

        try:
            tx = helper_functions.send_token(ergo=ergo, amount=amount, amount_tokens=amount_tokens, fee=self.miner_fee,
                                             receiver_addresses=receiver_addresses, tokens=tokens,
                                             wallet_mnemonic=self.seed_phrase)
            self.logger.info(f"Tokens sent successfully. TX: {tx}")
        except Exception as e:
            self.logger.error(f"Error sending tokens: {e}")
            tx = 'NOT ENOUGH LIQUIDITY'

        return tx

    def build_and_send(self, miner_wallet, payout, debug=True):
        payout = float(payout)
        self.logger.info("Debug mode: {}".format(debug))
        self.logger.info('{}, {}'.format(type(miner_wallet), type(payout)))
        self.logger.info(f"Building and sending transaction for miner: {miner_wallet}, payout: {payout}")
        miner_fee = 0.0012
        node_url: str = "http://213.239.193.208:9053/"
        ergo = appkit.ErgoAppKit(node_url=node_url)
        
        wallet_address = helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=self.seed_phrase)[0]

        token_data, ergo_data, results = self.get_token_data(miner_wallet, payout)
        results['miner'] = miner_wallet
        results['erg_balance_paid'] = payout
        if debug:
            print("Debug mode: Simulating transaction")
            self.logger.info("Debug mode: Simulating transaction")
            results['tx'] = 'debug'
            return token_data, ergo_data, results
            
        else:
            if not token_data:
                self.logger.info("Sending only ERG")
                tx = self.send_erg(ergo, miner_wallet, ergo_data['amount'])
            else:
                self.logger.info("Sending tokens and ERG")
                tx = self.send_tokens(ergo, ergo_data, token_data, miner_wallet)

            results['tx'] = str(tx)

            if tx == 'NOT ENOUGH LIQUIDITY':
                self.logger.warning("Not enough liquidity for transaction")
                return token_data, ergo_data, results
            
            self.logger.info(f'Submitted TX: {tx}')
            file = f'{miner_wallet}_TX.txt'
            with open(file, 'w') as f:
                with redirect_stdout(f):
                    print(tx)
            
            self.wait_for_tx_to_clear(tx)
            
            return token_data, ergo_data, results

        
                

        

        