import argparse
import sys
from utils import calculator

"""
Personal Finance Tracker - CLI tool for managing expenses and income
Usage: python finance.py [summary|add-expense][add-income] [args...]
"""


def main():
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")

    subparsers = parser.add_subparsers(
        title="command", dest="command", description="available commands")

    summary_parser = subparsers.add_parser('summary', help="Show financial summary")
    expense_parser = subparsers.add_parser("add-expense", help="Add expense")
    income_parser = subparsers.add_parser("add-income", help="Add income")
    list_parser = subparsers.add_parser("list", help="List recent transactions")

    expense_parser.add_argument("description", help="Description of the expense")
    expense_parser.add_argument("amount", type=float, help="Amount of the expense")
    expense_parser.add_argument("-c", "--category", default="General", help="Category of the expense (Optional)")

    income_parser.add_argument("description", help="Description of the income")
    income_parser.add_argument("amount", type=float, help="Amount of the income")
    income_parser.add_argument("-s", "--source", default="General", help="Source of the income (Optional)")

    list_parser.add_argument("--last", type=int, default=10,
                             help="Show only the last N transactions")

    args = parser.parse_args()

    if args.command == 'summary':
        summary = calculator.get_summary()
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
        # Call add_expense function
        expense = calculator.add_expense(
            args.description, args.amount, args.category)
        if expense:
            print(
                f"Added expense: {expense['description']} ${expense['amount']:,.2f} {expense['category']}")
        else:
            print("Failed to save expense")

    elif args.command == 'add-income':
        # Amount must always be positive
        if args.amount <= 0:
            print("Amount should have positive values")
            sys.exit(1)
        # Call add_expense function
        income = calculator.add_income(
            args.description, args.amount, args.source)
        if income:
            print(
                f"Added income: {income['description']} ${income['amount']:,.2f} {income['source']}")
        else:
            print("Failed to save income")
    elif args.command == 'list':
        calculator.list_transactions(args.last)


if __name__ == "__main__":
    main()
