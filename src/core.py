from src.builder import BuildTokenSwapTX

class SigsCore:
    def __init__(self):
        api = ''
        self.pool_addr = ''
        self.builder = BuildTokenSwapTX

    def update_minimum_payment(self):
        return 
        
    def check_for_payments(self):
        # read in balance df
        data = [{'miner': 'a', 'payout': 10},
                {'miner': 'b', 'payout': 5},]
                
        return data

    def send_payments(self):
        payment_addresses = self.check_for_payments()
        payment_data = []
        for sample in data:
            temp = {}
            address = sample['miner']
            payout = sample['payout']
            tx = self.builder.build_and_send(address, payout)
            
            temp{'miner'] = address
            temp['paid'] = payout
            temp['tx'] = tx
            payment_data.append(temp)

        return payment_data

    def update_data(self):

    def execute(self):
        self.update_minimum_payment()
        self.send_payments
        self.update_data()
        return
            

            

        