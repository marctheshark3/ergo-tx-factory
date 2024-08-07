from contextlib import redirect_stdout
from ergpy import appkit
from ergpy import helper_functions
from src.converter import ConvertTokens
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import time

class BuildTokenSwapTX:
    def __init__(self):
        self.converter = ConvertTokens()
        load_dotenv()
        self.seed_phrase = os.getenv('SWAP_MNEMONIC')
        self.miner_fee = 0.0012

    def get_api_data(self, api_url):
        try:
            # Send a GET request to the API
            response = requests.get(api_url)
    
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the response as JSON (assuming the API returns JSON data)
                data = response.json()
                return data
            else:
                print(f"Failed to retrieve data: Status code {response.status_code}")
                return None
    
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return None

    def get_token_data(self, miner_wallet, payout):
        df = pd.read_csv('https://raw.githubusercontent.com/marctheshark3/Mining-Reward-Tokens/main/supported-tokens.csv')
        results = self.converter.execute(miner_wallet, payout)

        token_data = []
        ergo_data = []
        print('results', results)
        for key in results.keys():
            
            value = results[key]
            temp_df = df[df['Token Name'] == key]
            data = {'tokenId': temp_df['Token ID'].values[0], 'amount': value, 'token': key}
            if key == 'ERGO':
                ergo_data = data
                continue
            token_data.append(data)
        return token_data, ergo_data

    def wait_for_tx_to_clear(self, tx):
        # this code should hold up any further TXs to be sent until the current one is cleared.
        api = 'https://api.ergoplatform.com/api/v1/transactions'
        tx_api = '{}/{}'.format(api, tx)
        done = False
        while True:
            
            
            print('Checking for confirmation of tx: {}'.format(tx))
            try:
                tx_data = self.get_api_data(tx_api)
                status = tx_data['id']
                print('TX CONFIRMED')
                break
                
            except Exception:
                print('TX UNconfirmed......Going to Go to Sleep!')
                time.sleep(120)
                continue
        

    def check_for_current_txs(self):
        while True:
            api = 'https://api.ergoplatform.com/api/v1/mempool/transactions/byAddress'
            tx_api = '{}/{}'.format(api, pool_address)
            data = get_api_data(tx_api)
        
            if data.items:
                continue
            else:
                break
            return

    def send_erg(self, ergo, rx, amount):
        receiver_addresses = [rx]
        amount = [amount]
        tx = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=self.seed_phrase,
                                              receiver_addresses=receiver_addresses, fee=self.miner_fee)
        return tx

    def send_tokens(self, ergo, ergo_data, token_data, rx):
        print(ergo_data, token_data, rx)
        tokens = [[token['tokenId']] for token in token_data] # how does this look if we have no tokens?
        amount_tokens = [[token['amount']] for token in token_data]
        receiver_addresses = [rx for _ in range(len(tokens))]

        if ergo_data:
            print('a')
            amount = [ergo_data['amount'] / len(tokens) for _ in range(len(tokens))] # amount of ergo tokens to send
            
        else:
            print('c')
            amount = [0.0001 for _ in range(len(tokens))]
        
        print(tokens, amount_tokens, amount, 'DATA VERIFICATION', token_data)

     
        tx = helper_functions.send_token(ergo=ergo, amount=amount, amount_tokens=amount_tokens, fee=self.miner_fee,
                              receiver_addresses=receiver_addresses, tokens=tokens,
                              wallet_mnemonic=self.seed_phrase)
        return tx
        

    def build_and_send(self, miner_wallet, payout):
        # self.wait_for_tx_to_clear(my_wallet)
        miner_fee = 0.0012 
        only_ergo = False
        node_url: str = "http://213.239.193.208:9053/"
        ergo = appkit.ErgoAppKit(node_url=node_url)
        
        wallet_address = helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=self.seed_phrase)[0]

        # lets assume for now we are always sending tokens
        print('gathering tokens')
        token_data, ergo_data = self.get_token_data(miner_wallet, payout)
        print('got the tokens')
        if not token_data:
            tx = self.send_erg(ergo, miner_wallet, ergo_data['amount'])
                               
        else:
            tx = self.send_tokens(ergo, ergo_data, token_data, miner_wallet)
                
        print('submited TX: {}'.format(tx))
        file = '{}_TX.txt'.format(miner_wallet)
        with open(file, 'w') as f:
            with redirect_stdout(f):
                print(tx)
                
        self.wait_for_tx_to_clear(tx)
        

        return


        
                

        

        