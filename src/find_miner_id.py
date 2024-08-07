import requests
import json 

class ReadTokens:
    def __init__(self, api='https://api.ergo.aap.cornell.edu/api/v1/boxes/byAddress', token_ls_url='https://api.ergo.aap.cornell.edu/api/v1/tokens/'):
        '''
        This code does a few things to find the latest miners ID:
        1. First we get the miners address and search for some known parameters that should be in the token
        2. From here we then look at block of when the token was first minted
        3. Then we check to see if miners address (current hold) was the address that minted this token

        '''
        
        self.api = api
        self.token_ls = token_ls_url

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
            
    def get_wallet_balance(self, wallet):
        url = 'http://213.239.193.208:9053/blockchain/balance'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, headers=headers, data=wallet)
        return response.json()

    
    def find_token_name_in_wallet(self, wallet, name):
        wallet_data = self.get_wallet_balance(wallet)

        tokens = wallet_data['confirmed']['tokens']
        ls = []
        for token in tokens:
            token_name = token['name']
            if token_name == name:
                ls.append(token)
        return ls

    def get_latest_miner_id(self, wallet):

        possible_tokens = self.find_token_name_in_wallet(wallet, 'Sigmanaut Mining Pool Miner ID - Season 0')
        for token in possible_tokens:
            token['height'] = self.get_token_description(token['tokenId'])['height']
        sorted_data = sorted(possible_tokens, key=lambda x: x['height'], reverse=True)
        ls = []
        for data in sorted_data:
            
            id = data['tokenId']
            height = data['height']
            base_url = 'https://api.ergoplatform.com/api/v1/boxes/byTokenId'
            url = '{}/{}'.format(base_url, id)
            api_data = self.get_api_data(url)
            ls.append(api_data)
            tx = None
            
            for data in api_data['items']:
                if height == data['creationHeight']:
                    tx = data['transactionId']
                    print(height, tx, id)
                    break
            # we now have the TX which created the NFT
            if tx:
                wallet_minted_tokens = []
                url = 'https://api.ergoplatform.com/api/v1/transactions'
                tx_url = '{}/{}'.format(url, tx)
                tx_data = self.get_api_data(tx_url)
                # print(data)
                box_id_first_input = tx_data['inputs'][0]['boxId']
                if box_id_first_input == id:
                    return id
                                    
    def get_token_description(self, id):
        # print(id, 'id')
        url = '{}/{}'.format(self.token_ls, id)
        data = self.get_api_data(url)

        token_description = json.loads(data['description'])
        return token_description

if __name__ == '__main__':
    url = 'https://api.ergo.aap.cornell.edu/api/v1/boxes/byAddress/'
    wallet = '9eg7v2nkypUZbdyvSKSD9kg8FNwrEdTrfC2xdXWXmEpDAFEtYEn'
    reader = ReadTokens(url, token_id)

    ids = reader.find_miner_id(wallet)