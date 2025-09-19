import argparse
import sys
from utils import calculator


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


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

    subparsers = parser.add_subparsers(title="command", dest="command", description="available commands")

    subparsers.add_parser('summary', aliases=["sum"], help="Show financial summary")
    subparsers.add_parser("add-expense", aliases=["exp"], help="Add expense")
    subparsers.add_parser("add-income", aliases=["inc"], help="Add income")
    subparsers.add_parser("list", aliases=["ls"], help="List recent transactions with optional filters")

    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)

    # quick parse to get command
    args_partial = parser.parse_known_args()[0]
    command = None
    if len(sys.argv) > 1:
        command = sys.argv[1]

    # Build command-specific parser
    if command in ('add-expense', 'exp'):
        parser_exp = argparse.ArgumentParser(add_help=False)
        parser_exp.add_argument('description')
        parser_exp.add_argument('amount', type=float)
        parser_exp.add_argument('-c', '--category', default='General')
        parsed = parser_exp.parse_args(sys.argv[2:])
        # validate
        if parsed.amount <= 0:
            print('Amount should have positive values')
            sys.exit(1)
        result = calculator.add_expense(parsed.description, parsed.amount, parsed.category)
        if not result.get('success'):
            print('Failed to add expense:', result.get('error'))
            sys.exit(1)
        t = result['transaction']
        print(f"Added expense: {t['description']} ${t['amount']:,.2f} {t['category']}")
        return

    if command in ('add-income', 'inc'):
        parser_inc = argparse.ArgumentParser(add_help=False)
        parser_inc.add_argument('description')
        parser_inc.add_argument('amount', type=float)
        parser_inc.add_argument('-s', '--source', default='General')
        parsed = parser_inc.parse_args(sys.argv[2:])
        if parsed.amount <= 0:
            print('Amount should have positive values')
            sys.exit(1)
        result = calculator.add_income(parsed.description, parsed.amount, parsed.source)
        if not result.get('success'):
            print('Failed to add income:', result.get('error'))
            sys.exit(1)
        t = result['transaction']
        print(f"Added income: {t['description']} ${t['amount']:,.2f} {t['source']}")
        return

    if command in ('summary', 'sum'):
        summary = calculator.get_summary()
        print(f"\n====== Financial Summary ======\n")
        print(f"{'Total income':<15}: {Colors.GREEN}${summary['total_income']:>12,.2f}{Colors.RESET}")
        print(f"{'Total expense':<15}: {Colors.RED}${summary['total_expense']:>12,.2f}{Colors.RESET}")
        print(f"{'Net balance':<15}: {Colors.YELLOW}${summary['net_balance']:>12,.2f}{Colors.RESET}")
        if summary['categories']:
            print(f"\n{Colors.BLUE}By Category:{Colors.RESET}")
            for k, v in summary['categories'].items():
                print(f"  {k:<15}: {Colors.RED}${v:>12,.2f}{Colors.RESET}")
        if summary['income_sources']:
            print(f"\n{Colors.BLUE}By Source:{Colors.RESET}")
            for k, v in summary['income_sources'].items():
                print(f"  {k:<15}: {Colors.GREEN}${v:>12,.2f}{Colors.RESET}")
        return

    if command in ('list', 'ls'):
        parser_ls = argparse.ArgumentParser(add_help=False)
        parser_ls.add_argument('--last', type=int, default=10)
        parser_ls.add_argument('--category')
        parser_ls.add_argument('--source')
        parser_ls.add_argument('--from-date')
        parser_ls.add_argument('--to-date')
        parsed = parser_ls.parse_args(sys.argv[2:])

        category_filter = parsed.category
        source_filter = parsed.source

        calculator.list_transactions(limit=parsed.last, category=category_filter, source=source_filter,
                                     from_date=parsed.from_date, to_date=parsed.to_date)
        return

    # No command or unknown
    parser.print_help()


if __name__ == '__main__':
    main()
