import argparse
import sys
from utils import calculator

"""
Personal Finance Tracker - CLI tool for managing expenses and income
Usage: python finance.py [summary|add-expense][add-income] [args...]
"""


class Colors:
    GREEN = "\033[92m"   # for income
    RED = "\033[91m"     # for expenses
    YELLOW = "\033[93m"  # for balance
    BLUE = "\033[94m"    # for headings or info
    RESET = "\033[0m"    # reset to default


def main():
    parser = argparse.ArgumentParser(
        description="Personal Finance Tracker",
        epilog="""Examples: python finance.py exp "Coffee" 5.50 -c Food
          python finance.py inc "Salary" 1000 -s Job
  python finance.py sum
  python finance.py ls --last 5
  python finance.py ls --category Food
  python finance.py ls --from-date 2025-09-01 --to-date 2025-09-18
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(
        title="command", dest="command", description="available commands")

    summary_parser = subparsers.add_parser('summary', aliases=["sum"], help="Show financial summary")
    expense_parser = subparsers.add_parser("add-expense", aliases=["exp"], help="Add expense")
    income_parser = subparsers.add_parser("add-income", aliases=["inc"], help="Add income")
    list_parser = subparsers.add_parser("list", aliases=["ls"], help="List recent transactions with optional filters")

    expense_parser.add_argument("description", help="Description of the expense")
    expense_parser.add_argument("amount", type=float, help="Amount of the expense")
    expense_parser.add_argument("-c", "--category", default="General", help="Category of the expense (Optional)")

    income_parser.add_argument("description", help="Description of the income")
    income_parser.add_argument("amount", type=float, help="Amount of the income")
    income_parser.add_argument("-s", "--source", default="General", help="Source of the income (Optional)")

    list_parser.add_argument("--last", type=int, default=10,
                             help="Show only the last N transactions (default: 10)")
    list_parser.add_argument("--category", help="Filter by category (for expenses) or source (for income)")
    list_parser.add_argument("--from-date", help="Filter transactions from this date (YYYY-MM-DD)")
    list_parser.add_argument("--to-date", help="Filter transactions up to this date (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == 'summary':
        summary = calculator.get_summary()
        # Format numbers with commas, 2 decimals, and align in a neat column
        print(f"\n====== Financial Summary ======\n")
        print(f"{'Total income':<15}: {Colors.GREEN}${summary['total_income']:>12,.2f}{Colors.RESET}")
        print(f"{'Total expense':<15}: {Colors.RED}${summary['total_expense']:>12,.2f}{Colors.RESET}")
        print(f"{'Net balance':<15}: {Colors.YELLOW}${summary['net_balance']:>12,.2f}{Colors.RESET}")

        # Print category breakdown if available
        if "categories" in summary and summary["categories"]:
            print(f"\n{Colors.BLUE}By Category:{Colors.RESET}")
            for category, amount in summary["categories"].items():
                print(f"  {category:<15}: {Colors.RED}${amount:>12,.2f}{Colors.RESET}")

        if "income_sources" in summary and summary["income_sources"]:
            print(f"\n{Colors.BLUE}By Source:{Colors.RESET}")
            for source, amount in summary["income_sources"].items():
                print(f"  {source:<15}: {Colors.GREEN}${amount:>12,.2f}{Colors.RESET}")
            print()

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
        calculator.list_transactions(args.last, args.category, args.from_date, args.to_date)


if __name__ == "__main__":
    main()
