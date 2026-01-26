import json
import os

DATA_FILE = "data.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)
