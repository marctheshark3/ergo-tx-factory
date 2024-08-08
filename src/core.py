import logging
from src.builder import BuildTokenSwapTX
from src.database import PostgresDB
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='sigs_core.log')
logger = logging.getLogger(__name__)

class SigsCore:
    def __init__(self):
        self.pool_addr = ''
        self.builder = BuildTokenSwapTX()
        self.db = PostgresDB()
        self.logger = logging.getLogger(__name__)

    def update_minimum_payment(self):
        self.logger.info('Updating minimum payment')
        # Implement your logic here
        return 
        
    def check_for_payments(self):
        try:
            balances_data = self.db.fetch_data('balances')
            columns = self.db.get_column_names('balances')
            df = pd.DataFrame(balances_data, columns=columns)
            
            df['send_payment'] = (df['balance'] >= df['min_payout']).astype(int)
            send_df = df[df['send_payment'] == 1]
            
            self.logger.info(f"Found {len(send_df)} payments to process")
            return send_df
        except Exception as e:
            self.logger.error(f"Error in check_for_payments: {str(e)}")
            return pd.DataFrame()

    def send_payments(self, df, debug=True):
        payment_data = []
        data = []
        for _, row in df.iterrows():
            try:
                address = row['address']
                payout = row['balance']
                
                self.logger.info(f"Sending payment of {payout} to {address}")
                token_data, ergo_data, results = self.builder.build_and_send(address, payout, debug=debug)
                
                token_data.append(ergo_data)
                payment_data.append(row)
                data.append(results)
            except Exception as e:
                self.logger.error(f"Error sending payment to {address}: {str(e)}")
        return pd.DataFrame(data)

    def update_data(self, df): 
        df.to_csv('payments.csv')
        self.logger.info('Updating data')
        payment_records = []
        for _, row in df.iterrows():
            for asset, amount in row.items():
                if asset not in ['miner', 'erg_balance_paid', 'tx']:
                    print(amount, 'ammnt')
                    
                    payment_record = {
                        'Asset': asset,
                        'Amount': amount,
                        'address': row['miner'],
                        'Balance_Paid': row['erg_balance_paid'],
                        'TransactionId': row['tx']
                    }
                    if pd.isna(amount):
                        print('triggered')
                        self.logger.warning(f"NaN amount detected for asset {asset} to miner {row['miner']}. Skipping this record.")
                        continue
                    else:
                        payment_records.append(payment_record)
                    
                    try:
                        self.db.insert_data('payments', payment_record)
                        self.logger.info(f"Inserted payment record for {row['miner']}")
                        
                        # Update balance to 0 if transaction is valid
                        invalid_txs = ['', 'NOT ENOUGH LIQUIDITY']
                        if payment_record['TransactionId'] not in invalid_txs: # need to add not
                            self.db.execute_query(f"UPDATE balances SET balance = 0 WHERE address = '{payment_record['address']}'")
                            self.logger.info(f"Updated balance for {payment_record['address']} to 0")
                    except Exception as e:
                        self.logger.error(f"Error processing payment record: {str(e)}")
        
        return pd.DataFrame(payment_records)

    def execute(self, debug=True):
        try:
            self.logger.info("Starting payment execution")
            self.update_minimum_payment()
            payments = self.check_for_payments()
            if not payments.empty:
                data = self.send_payments(payments, debug)
                df = self.update_data(data)
                self.logger.info("Payment execution completed successfully")
                return df
            else:
                self.logger.info("No payments to process")
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error in execute method: {str(e)}")
            return pd.DataFrame()