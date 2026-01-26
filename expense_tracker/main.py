from expense import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense
)
from report import show_reports


def show_menu():
    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Reports")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            edit_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            show_reports()

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
