from utils import storage
from datetime import datetime


def validate_input(description, amount, extra_value, extra_key_name):
    labels = {
        "description": "Description",
        "amount": "Amount",
        "category": "Category",
        "source": "Source"
    }

    data_to_check = {
        "description": description,
        "amount": amount,
        extra_key_name: extra_value
    }

    rule_validation = {
        "description": "non_empty_string",
        "amount": "positive number",
        extra_key_name: "non_empty_string"
    }

    for key, value in data_to_check.items():
        rule = rule_validation[key]

        if rule == "non_empty_string":
            if not isinstance(value, str) or not value.strip():
                return {"success": False, "error": f"{labels[key]} must not be empty."}
        elif rule == "positive number":
            if not isinstance(value, (int, float)) or value <= 0:
                return {"success": False, "error": f"{labels[key]} must be a positive number."}

    return {"success": True}


def add_expense(description, amount, category="General"):
    validation_result = validate_input(description, amount, category, "category")
    if not validation_result["success"]:
        return validation_result

    date_time = datetime.now()
    data = storage.load_data()

    new_id = max((t["id"] for t in data["transactions"]), default=0) + 1
    new_expense = {
        "id": new_id,
        "type": "expense",
        "description": description,
        "amount": amount,
        "category": category or "General",
        "date": date_time.strftime("%Y-%m-%d")
    }

    data["transactions"].append(new_expense)
    return new_expense if storage.save_data(data) else False


def add_income(description, amount, source="General"):
    validation_result = validate_input(description, amount, source, "source")
    if not validation_result["success"]:
        return validation_result

    date_time = datetime.now()
    data = storage.load_data()

    new_id = max((t["id"] for t in data["transactions"]), default=0) + 1
    new_income = {
        "id": new_id,
        "type": "income",
        "description": description,
        "amount": amount,
        "source": source or "General",
        "date": date_time.strftime("%Y-%m-%d")
    }

    data["transactions"].append(new_income)
    return new_income if storage.save_data(data) else False


def get_all_expenses():
    data = storage.load_data()
    return [t for t in data["transactions"] if t["type"].lower() == "expense"]


def get_all_income():
    data = storage.load_data()
    return [t for t in data["transactions"] if t["type"].lower() == "income"]


def get_summary():
    data = storage.load_data()
    if not data["transactions"]:
        return {"total_income": 0.0, "total_expense": 0.0, "net_balance": 0.0, "categories": {}}

    total_income = sum(float(t["amount"]) for t in data["transactions"] if t["type"].lower() == "income")
    total_expense = sum(float(t["amount"]) for t in data["transactions"] if t["type"].lower() == "expense")

    categories = {}
    for t in data["transactions"]:
        if t["type"].lower() == "expense":
            categories[t["category"]] = categories.get(t["category"], 0.0) + float(t["amount"])

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "categories": categories
    }


def get_specific_category(category):
    data = storage.load_data()
    if not category:
        return data["transactions"]

    filtered = [t for t in data["transactions"] if t.get("category", "").lower() == category.lower()]
    return filtered if filtered else "Category not found"
