from utils import storage
from datetime import datetime

def validate_input(description, amount, category):
    data_to_check = {
        "description": description,
        "amount": amount,
        "category": category
    }

    rule_validation = {
        "description": "non_empty_string",
        "amount":  "positive number",
        "category": "non_empty_string"
    }

    for key, value in data_to_check.items():
        rule = rule_validation[key]

        if rule == "non_empty_string":
            if not isinstance(value, str) or not value.strip():
                return {"success": False, "error": f"{key.title()} must not be an empty string."}
        elif rule == "positive number":
            if not isinstance(value, (int, float)) or value <= 0:
                return {"success": False, "error": f"{key.title()} must not be less than 0"}

    return {"success": True}

def add_expense(description, amount, category="General"):
    # Validate inputs
    validation_result = validate_input(description,amount,category)

    if not validation_result["success"]:
        return validation_result

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
    #Validate inputs
    validation_result = validate_input(description, amount, category)

    if not validation_result["success"]:
        return validation_result

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

def get_specific_category(category):
    if not category:
        return storage.data["transactions"]

    #Load the data
    data = storage.load_data()

    #Create empty list to store category found in transaction
    categories = []

    for transaction in data["transactions"]:
        if transaction["category"].lower() == category.lower():
            categories.append(transaction)

    if not categories:
        return "Category not found"
    else:
        return categories


