import json
import os

DATA_FILE = "data.json"


def initialize_storage():
    """
    Create data.json if it does not exist.
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)


def load_expenses():
    """
    Load all expenses from data.json.
    Returns a list of expense dictionaries.
    """
    initialize_storage()

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If file is corrupted, reset safely
        return []


def save_expenses(expenses):
    """
    Save the entire expenses list to data.json.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)
