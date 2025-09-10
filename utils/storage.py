import json
import os

# Use script’s location to find transactions.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "transactions.json")


def load_data():
    # Check if file exists
    if os.path.exists(DATA_FILE):

        # If exists: read JSON file and return data
        with open(DATA_FILE, "r") as file:
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
        return {"transactions": []}


def save_data(data):
    # Write data dictionary to JSON file
    with open(DATA_FILE, "w") as file:
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
