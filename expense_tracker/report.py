from storage import load_expenses

def show_reports():
    expenses = load_expenses()

    if not expenses:
        print("📭 No expenses found.")
        return

    total = 0
    category_totals = {}
    highest = expenses[0]

    for exp in expenses:
        amount = exp["amount"]
        category = exp["category"]

        total += amount

        category_totals[category] = category_totals.get(category, 0) + amount

        if amount > highest["amount"]:
            highest = exp

    print("\n📊 ===== Expense Report =====")
    print(f"💰 Total Spent: ₹{total}")

    print("\n📂 Category-wise totals:")
    for cat, amt in category_totals.items():
        print(f"  - {cat}: ₹{amt}")

    print("\n🔥 Highest Expense:")
    print(f"  ₹{highest['amount']} | {highest['category']} | {highest['note']}")
