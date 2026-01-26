TASK_FILE = "tasks.txt"


def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nYour tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


def add_task(tasks):
    task = input("Enter new task: ").strip()
    if not task:
        print("Task cannot be empty.")
        return

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    try:
        index = int(input("Enter task number to delete: "))
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f"Removed task: {removed}")
    except (ValueError, IndexError):
        print("Invalid input.")


def main():
    tasks = load_tasks()
    print("Welcome to To-Do CLI App")

    while True:
        print("\n1. View tasks\n2. Add task\n3. Delete task\n4. Exit")
        choice = input("Choose (1-4): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
