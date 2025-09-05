import argparse
import sys

"""
Personal Finance Tracker - CLI tool for managing expenses and income
Usage: python finance.py [summary|add-expense] [args...]
"""


def main():
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")

    subparsers = parser.add_subparsers(
        title="command", dest="command", description="available commands")

    summary_parser = subparsers.add_parser('summary', help="Show financial summary")
    expense_parser = subparsers.add_parser("add-expense", help="Add expense")

    expense_parser.add_argument("description", help="Description of the expense")
    expense_parser.add_argument("amount", type=float, help="Amount of the expense")

    args = parser.parse_args()

    if args.command == 'summary':
        print("Total Income: $0")
        print("Total Expenses: $0")
        print("Balance: $0")
    elif args.command == 'add-expense':
        # Amount must always be positive
        if args.amount <= 0:
            print("Amount should have positive values")
            sys.exit(1)
        print(f"Added expense: {args.description} ${args.amount}")


if __name__ == "__main__":
    main()
