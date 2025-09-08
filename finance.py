import argparse
import sys
from utils import storage

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
        summary = storage.get_summary()
        # Format numbers with commas, 2 decimals, and align in a neat column
        print("\n--- Financial Summary ---")
        print(f"Total income  :  ${summary['total_income']:,.2f}")
        print(f"Total expense :  ${summary['total_expense']:,.2f}")
        print(f"Net balance   :  ${summary['net_balance']:,.2f}")

        # Print category breakdown if available
        if "categories" in summary and summary["categories"]:
            print("\nBy Category:")
            for category, amount in summary["categories"].items():
                # Left-align category names (width 12), right-align amounts
                print(f"  {category:<12}:  ${amount:,.2f}\n")
    elif args.command == 'add-expense':
        # Amount must always be positive
        if args.amount <= 0:
            print("Amount should have positive values")
            sys.exit(1)
        print(f"Added expense: {args.description} ${args.amount}")


if __name__ == "__main__":
    main()
