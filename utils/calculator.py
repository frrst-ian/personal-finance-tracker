from utils import storage
from datetime import datetime


def add_expense(description, amount, category="General"):
    date_time = datetime.now()
    # Load existing data
    data = storage.load_data()

    if data["transactions"]:
        new_id = max(transaction["id"] for transaction in data["transactions"]) + 1
    else:
        new_id = 1
    # Create new expense entry with current timestamp
    new_expense = {
        "id": new_id,
        "type": "expense",
        "description": description,
        "amount": amount,
        "category": category or "General",
        "date": date_time.strftime("%Y-%m-%d")
    }

    # Append to expenses list
    data["transactions"].append(new_expense)
    # Save updated data
    success = storage.save_data(data)
    if success:
        return new_expense   # return the expense dict
    else:
        return False         # or None


def add_income(description, amount, category):
    date_time = datetime.now()
    # Load existing data
    data = storage.load_data()

    if data["transactions"]:
        new_id = max(transaction["id"] for transaction in data["transactions"]) + 1
    else:
        new_id = 1

    # Create new expense entry with current timestamp
    new_income = {
        "id": new_id,
        "type": "income",
        "description": description,
        "amount": amount,
        "category": category,
        "date": date_time.strftime("%Y-%m-%d")
    }

    # Append to expenses list
    data["transactions"].append(new_income)
    # Save updated data
    success = storage.save_data(data)
    if success:
        return new_income   # return the expense dict
    else:
        return False         # or None


def get_all_expenses():

    # Load data
    data = storage.load_data()
    # Return expenses list
    expenses = []
    for transaction in data["transactions"]:
        if transaction["type"].lower() == "expense":
            expenses.append(transaction)

    return expenses


def get_all_income():

    # Load data
    data = storage.load_data()

    # Return income list
    income = []
    for transaction in data["transactions"]:
        if transaction["type"].lower() == "income":
            income.append(transaction)

    return income


def get_summary():
    """
    Calculate and return a financial summary:
    - Total income
    - Total expense
    - Net balance (income - expense)
    - Optional breakdown by expense category
    """

    data = storage.load_data()

    if not data["transactions"]:
        # No transactions yet → return all zeros
        return {
            "total_income": 0.0,
            "total_expense": 0.0,
            "net_balance": 0.0,
            "categories": {}
        }

    # Ensure consistent handling of income/expense
    total_income = sum(float(t["amount"])
                       for t in data["transactions"] if t["type"].lower() == "income")
    total_expense = sum(float(t["amount"])
                        for t in data["transactions"] if t["type"].lower() == "expense")

    # Optional: breakdown of expenses by category
    categories = {}
    for t in data["transactions"]:
        if t["type"].lower() == "expense":
            categories[t["category"]] = categories.get(t["category"], 0.0) + float(t["amount"])

    # Net balance = income - expense
    net_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "categories": categories
    }
