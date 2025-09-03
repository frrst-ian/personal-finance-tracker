import argparse


def main():
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")
    subparsers = parser.add_subparsers(dest="command")

    summary_parser = subparsers.add_parser('summary', help="Show financial summary")

    args = parser.parse_args()

    if(args.command == 'summary'):
        print("Total Income: $0")
        print("Total Expenses: $0")
        print("Balance: $0")


if __name__ == "__main__":
    main()
