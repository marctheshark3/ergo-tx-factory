from contextlib import redirect_stdout
from ergpy import appkit
from ergpy import helper_functions
from src.converter import ConvertTokens
import os
from dotenv import load_dotenv
import pandas as pd

class BuildTokenSwapTX:
    def __init__(self):
        self.converter = ConvertTokens()
        load_dotenv()
        self.seed_phrase = os.getenv('SWAP_MNEMONIC')

    def get_token_data(self, miner_wallet):
        df = pd.read_csv('https://raw.githubusercontent.com/marctheshark3/Mining-Reward-Tokens/main/supported-tokens.csv')
        results = self.converter.execute(miner_wallet)

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
        return token_data, ergo_data

    def build_and_send(self, my_wallet, miner_wallet):
        node_url: str = "http://213.239.193.208:9053/"
        ergo = appkit.ErgoAppKit(node_url=node_url)
        
        wallet_address = helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=self.seed_phrase)[0]

        # lets assume for now we are always sending tokens
        token_data, ergo_data = self.get_token_data(miner_wallet)
        
        tokens = [[token['tokenId']] for token in token_data]
        amount_tokens = [[token['amount']] for token in token_data]
        receiver_addresses = [miner_wallet for _ in range(len(tokens))]

        if ergo_data:
            amount = [ergo_data['amount'] / len(tokens) for _ in range(len(tokens))] # amount of ergo tokens to send
        else:
            amount = [0.0001 for _ in range(len(tokens))]

        # print(tokens, amount_tokens, amount, 'DATA VERIFICATION', token_data)

        output_main = helper_functions.send_token(ergo=ergo, amount=amount, amount_tokens=amount_tokens,
                                  receiver_addresses=receiver_addresses, tokens=tokens,
                                  wallet_mnemonic=self.seed_phrase)
        
        file = '{}_TX.txt'.format(my_wallet)
        with open(file, 'w') as f:
            with redirect_stdout(f):
                print(output_main)
        
        helper_functions.exit()
        return


        
                

        

        