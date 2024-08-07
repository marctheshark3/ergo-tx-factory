import argparse
from src.builder import BuildTokenSwapTX

def main(my_wallet, miner_wallet):
    builder = BuildTokenSwapTX()
    try:
        builder.build_and_send(my_wallet, miner_wallet, payout=5)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build and send a token swap transaction.')
    parser.add_argument('--my_wallet', type=str, required=True, help='Your wallet address')
    parser.add_argument('--miner_wallet', type=str, required=True, help='Miner wallet address')

    args = parser.parse_args()

    main(args.my_wallet, args.miner_wallet)


