VALID_STATUSES = ["Applied", "Interview", "Rejected", "Offer"]


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(" Please enter a value.")


def choose_status(prompt: str = "Choose status") -> str:
    print(f"\n{prompt}:")
    for i, s in enumerate(VALID_STATUSES, start=1):
        print(f"{i}. {s}")

    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(VALID_STATUSES):
            return VALID_STATUSES[int(choice) - 1]
        print("Invalid choice. Try again.")


def pause():
    input("\nPress Enter to continue...")
