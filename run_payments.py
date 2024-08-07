from src.core import SigsCore

def main():
    robot = SigsCore()
    df = robot.execute(debug=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if a miner has an over due balance and if so send it!')

    main()
