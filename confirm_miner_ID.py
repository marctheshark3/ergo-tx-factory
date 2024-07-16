import argparse
from src.converter import ConvertTokens

def main(miner_wallet):
    reader = ConvertTokens()
    miner_id = reader.get_miner_id(miner_wallet)

    if miner_id:
        print('MINER DOES HAVE MINER ID')
        return miner_id['minimumPayout']

    print('MINER DID NOT HAVE MINER ID')
    return miner_id
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Determine if the miner has a miner id and if so return their minimum payout')
   
    parser.add_argument('--miner_wallet', type=str, required=True, help='Miner wallet address')

    args = parser.parse_args()

    main(args.miner_wallet)


