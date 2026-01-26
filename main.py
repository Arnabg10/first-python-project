def greet_user(name, times):
    for i in range(1, times + 1):
        print(f"Hello {name} 👋 ({i})")


def main():
    name = input("Enter your name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        times = int(input("How many times should I greet you? "))
        if times <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    print()
    greet_user(name, times)


if __name__ == "__main__":
    main()
