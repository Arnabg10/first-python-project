from storage import load_expenses, save_expenses


def add_expense():
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    category = input("Enter category: ").strip()
    note = input("Enter note (optional): ").strip()

    expense = {
        "amount": amount,
        "category": category,
        "note": note
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)

    print("✅ Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("📭 No expenses found.")
        return

    print("\n📋 Your Expenses:")
    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx}. ₹{exp['amount']} | {exp['category']} | {exp['note']}")


def edit_expense():
    expenses = load_expenses()

    if not expenses:
        print("📭 No expenses to edit.")
        return

    view_expenses()

    try:
        index = int(input("Enter expense number to edit: ")) - 1
        if index < 0 or index >= len(expenses):
            print("❌ Invalid selection.")
            return
    except ValueError:
        print("❌ Enter a valid number.")
        return

    try:
        new_amount = float(input("New amount: "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    new_category = input("New category: ").strip()
    new_note = input("New note: ").strip()

    expenses[index] = {
        "amount": new_amount,
        "category": new_category,
        "note": new_note
    }

    save_expenses(expenses)
    print("✏️ Expense updated successfully!")


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("📭 No expenses to delete.")
        return

    view_expenses()

    try:
        index = int(input("Enter expense number to delete: ")) - 1
        if index < 0 or index >= len(expenses):
            print("❌ Invalid selection.")
            return
    except ValueError:
        print("❌ Enter a valid number.")
        return

    deleted = expenses.pop(index)
    save_expenses(expenses)

    print(f"🗑️ Deleted expense ₹{deleted['amount']} ({deleted['category']})")
