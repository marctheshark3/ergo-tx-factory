from src.find_miner_id import ReadTokens
import pandas as pd

import sys



class ConvertTokens:
    def __init__(self):
        self.reader = ReadTokens()
        
    def get_miner_id(self, wallet):
        token = self.reader.get_latest_miner_id(wallet)
        try:
            miner_id = self.reader.get_token_description(token['tokenId'])
        except TypeError:
            return None

        # print('MINER ID: {}'.format(miner_id))
        return miner_id

    def get_token_conversions(self, wallet, miner_id):
        spectrum_price_data = self.reader.get_api_data('https://api.spectrum.fi/v1/price-tracking/markets')
        tokens_to_swap = [item['token'] for item in miner_id['tokens']]
        
        my_spectrum_data = []
        swap = {}
        for data in spectrum_price_data:
            token = data['quoteSymbol']
            if data['baseSymbol'] == 'ERG' and token in tokens_to_swap:                
                swap[token] = data['lastPrice']
            if 'ERGO' in tokens_to_swap:
                swap['ERGO'] = 1
        return swap

    def create_conversion(self, miner_id, price_conversion):
        conversions = {}
        payout = miner_id['minimumPayout']
        
        for item in miner_id['tokens']:    
            token = item['token']
            ratio = item['value']
            ergs_to_swap = payout * ratio / 100
            try:
                token_conversion = price_conversion[token]
                conversions[token] = token_conversion * ergs_to_swap
            except KeyError:
                print('The TOKEN {} ISNT SUPPORTED on SPECTRUM'.format(token))
        return conversions

    def execute(self, wallet):
        miner_id = self.get_miner_id(wallet)
        price_conversion = self.get_token_conversions(wallet, miner_id)
        return self.create_conversion(miner_id, price_conversion)

        