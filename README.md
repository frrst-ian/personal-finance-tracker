# Personal Finance Tracker

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)]()

A simple command-line tool for tracking personal expenses and income with color-coded output and filtering capabilities.

## Installation

```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

No additional dependencies required - uses Python standard library only.

## Usage

### Add Transactions
```bash
# Add expense
python finance.py exp "Coffee" 5.50 -c Food
python finance.py add-expense "Gas" 45.00 -c Transport

# Add income
python finance.py inc "Salary" 2500 -s Job
python finance.py add-income "Freelance" 500 -s "Side Hustle"
```

### View Summary
```bash
python finance.py summary
# or
python finance.py sum
```

### List Transactions
```bash
# Show last 10 transactions (default)
python finance.py ls

# Show last 5 transactions
python finance.py ls --last 5

# Filter by category/source
python finance.py ls --category Food

# Filter by date range
python finance.py ls --from-date 2025-09-01 --to-date 2025-09-18
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `add-expense` | `exp` | Add a new expense |
| `add-income` | `inc` | Add a new income |
| `summary` | `sum` | Show financial summary |
| `list` | `ls` | List recent transactions |

## Data Storage

Transactions are stored in `data/transactions.json` and persist between sessions.

## Contributors

- **Ian Forrest** - [@frrst-ian](https://github.com/frrst-ian)
- **Jude Melvin Grutas** - [@Grutz09](https://github.com/Grutz09)

## License

MIT License - see [LICENSE](LICENSE) file for details.