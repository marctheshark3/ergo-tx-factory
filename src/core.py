from src.builder import BuildTokenSwapTX
import pandas as pd

class SigsCore:
    def __init__(self):
        api = ''
        self.pool_addr = ''
        self.builder = BuildTokenSwapTX()

    def update_minimum_payment(self):
        print('updating minimum payment')
        return 
        
    def check_for_payments(self):
        # read in balance df
        data = [{'miner': '9eg7v2nkypUZbdyvSKSD9kg8FNwrEdTrfC2xdXWXmEpDAFEtYEn',
                 'min_payout': 1,'balance': 10},
                {'miner': '9fj3mV8aF27jZBBH5HBdecVcD5hoUcqqcMmo1j8aUbCA1rceGLE',
                 'min_payout': 0.01, 'balance': 0.1},
                {'miner': '9hAcdWpFAv7biCSeUcCvXWYRfEepm1ubdsfg5PC48k9S7ymiU3W',
                 'min_payout': 1.5,'balance': 0.2}]

        df = pd.DataFrame(data)
        df['send_payment'] = (df['balance'] >= df['min_payout']).astype(int)
        send_df = df[df['send_payment'] == 1]
                
        return send_df

    def send_payments(self, df, debug=True):
        payment_data = []
        data = []
        for _, row in df.iterrows():
            temp = {}
            address = row['miner']
            payout = row['balance']
            
            token_data, ergo_data, results = self.builder.build_and_send(address, payout, debug=debug)
            
            token_data.append(ergo_data)
            payment_data.append(row)
            data.append(results)
        df = pd.DataFrame(df)
        return data

    def update_data(self, data): 
        print('updating data')
        ls = []
        erg_ls = ['ERGO', 'miner', 'erg_balance_paid', 'tx']
        for item in data:
            keys = list(item.keys())
            tokens = [key for key in keys if key not in erg_ls]
            if 'ERGO' in keys:
                ls.append(['ERGO', item['ERGO'], item['miner'], item['erg_balance_paid'], item['tx']])
        
            for token in tokens:
                ls.append([token, item[token], item['miner'], item['erg_balance_paid'], item['tx']])
        # Specify the column names
        columns = ['Asset', 'Amount', 'Miner', 'Balance Paid', 'TransactionId']
        
        # Create the DataFrame
        df = pd.DataFrame(ls, columns=columns)
        return df

 
    def execute(self, debug=True):
        self.update_minimum_payment()
        payments = self.check_for_payments()
        if not payments.empty:
            data = self.send_payments(payments, debug)
            df = self.update_data(data)
        return df
            

            

        