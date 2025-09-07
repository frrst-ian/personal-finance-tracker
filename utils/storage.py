import json
from datetime import datetime
import os

# data = open("../data/transactions.json", "r")

def load_data():
# Check if file exists
    if os.path.exists("../data/transactions.json"):

# If exists: read JSON file and return data
        with open("../data/transactions.json", "r") as file:
            # Handle JSON decode errors
            try:
                data = json.load(file)
                return data
            except ValueError as e:
                print(f"Error: The transactions file is corrupted and cannot be read: {e}")
                print("Starting with empty transactions. Your file may need to be restored from backup.")
                return {"transactions": []}

# If not exists: return default structure with empty expenses/income lists
    else:
        print("Starting with empty transaction.")
        return {"transactions":[]}

def save_data(data):
# Write data dictionary to JSON file
    with open("../data/transactions.json", "w") as file:
        # Handle file write errors
        try:
            json.dump(data, file, indent=2)
            return True
        except (IOError, OSError, PermissionError) as e:
            print(f"Error writing file: {e}")
            return False
        except (TypeError, ValueError) as e:
            print(f"Error converting data to JSON: {e}")
            return False
# Maybe backup existing file first

def add_expense(description, amount, category):
    date_time = datetime.now()
    # Load existing data
    data = load_data()

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
        "category": category,
        "date": date_time.strftime("%Y-%m-%d")
    }

    # Append to expenses list
    data["transactions"].append(new_expense)
    # Save updated data
    success = save_data(data)
    # Return success/failure
    return success

def add_income(description, amount, category):
    date_time = datetime.now()
    # Load existing data
    data = load_data()

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
    success = save_data(data)
    # Return success/failure
    return success

def get_all_expenses():

    # Load data
    data = load_data()
    # Return expenses list
    expenses = []
    for transaction in data["transactions"]:
        if transaction["type"].lower() == "expense":
            expenses.append(transaction)

    return expenses

def get_all_income():

    # Load data
    data = load_data()

    # Return income list
    income = []
    for transaction in data["transactions"]:
        if transaction["type"].lower() == "income":
            income.append(transaction)

    return income

def get_summary():
    # Load data
    data = load_data()

    # Calculate total income, total expenses, net balance
    total_income = 0
    total_expense = 0
    for transaction in data["transactions"]:
        if transaction["type"] == "Income":
            total_income = total_income + transaction["amount"]
        elif transaction["type"] == "Expense":
            total_expense = total_expense + transaction["amount"]

    net_balance = total_income - total_expense

    summary_dict = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    }
    # Return summary dictionary
    return summary_dict

 ##### FOR DEBUGGING
    # print("Loaded data:", data)
    # print("Number of transactions:", len(data["transactions"]))
    # for transaction in data["transactions"]:
    #     print("Transaction type:", transaction.get("type"))
#####
