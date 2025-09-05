import json
from datetime import datetime

def view_summary():
    with open("../data/transactions.json", "r"):
        for transaction in data["transactions"]:
            print(json.dumps(transaction, indent=2))


with open("../data/transactions.json", "r") as file:
     data = json.load(file)

transaction_type = input("Expense/ Income/ View Summary/ List Transaction\nEnter transaction type: ")

if transaction_type == "View Summary":
    view_summary()

description = input("Enter description: ")
amount = input("Enter amount: ")
category = input("Enter category (e.g Food, School Supplies, etc.: ")
date = input("Enter date: ")

try:
    valid_date = datetime.strptime(date, "%Y-%m-%d")
    print("Valid Date:", valid_date.date())
except ValueError:
    print("Invalid format. Please use YYYY-MM-DD.")

new_transaction = {
    "id": len(data["transactions"]) + 1,
    "type": transaction_type,
    "description": description,
    "amount": amount,
    "category": category,
    "date": date
}

data["transactions"].append(new_transaction)

with open("../data/transactions.json", "w") as file:
    json.dump(data, file, indent=2)