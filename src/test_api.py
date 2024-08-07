# test_api.py

import requests
import pandas as pd
from pprint import pprint

BASE_URL = 'http://127.0.0.1:5000/sigs-core'

def test_api(table_name, params=None):
    url = f'{BASE_URL}/{table_name}'
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        print(f"\nData from {table_name} table:")
        print(df)
        return df
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Test balances table
print("Testing balances table:")
balances_df = test_api('balances')

# Test payments table
print("\nTesting payments table:")
payments_df = test_api('payments')

# Test with conditions (e.g., get payments for a specific asset)
print("\nTesting payments table with condition (Asset = 'ERGO'):")
ergo_payments_df = test_api('payments', {'Asset': 'ERGO'})

# Test with multiple conditions
print("\nTesting balances table with multiple conditions (balance > 5 and min_payout < 1):")
high_balance_df = test_api('balances', {'balance': '>5', 'min_payout': '<1'})