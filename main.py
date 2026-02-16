from tracker import JobTracker
from utils import input_non_empty, choose_status, pause


def print_applications(apps):
    if not apps:
        print("\n(No applications found.)")
        return

    print("\nID  Company           Role              Location          Status      Applied")
    print("-" * 78)
    for a in apps:
        print(f"{a.id:<3} {a.company:<16} {a.role:<17} {a.location:<16} {a.status:<10} {a.applied_date}")
        if a.notes:
            print(f"    Notes: {a.notes}")


def main():
    tracker = JobTracker()

    while True:
        print("\n=== Job Application Tracker ===")
        print("1. Add new application")
        print("2. View all applications")
        print("3. Update status")
        print("4. Filter by status")
        print("5. Delete application")
        print("6. Show stats")
        print("7. Search by company")
        print("0. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            company = input_non_empty("Company: ")
            role = input_non_empty("Role: ")
            location = input_non_empty("Location: ")
            status = choose_status("Select status")
            notes = input("Notes (optional): ").strip()

            app = tracker.add(company, role, location, status, notes)
            print(f"\n✅ Added application with ID {app.id}")
            pause()

        elif choice == "2":
            print_applications(tracker.list_all())
            pause()

        elif choice == "3":
            app_id = input("Enter application ID: ").strip()
            if not app_id.isdigit():
                print(" ID must be a number.")
                pause()
                continue
            new_status = choose_status("Update to which status")
            ok = tracker.update_status(int(app_id), new_status)
            print("✅ Updated." if ok else "ID not found.")
            pause()

        elif choice == "4":
            status = choose_status("Filter by which status")
            apps = tracker.filter_by_status(status)
            print_applications(apps)
            pause()

        elif choice == "5":
            app_id = input("Enter application ID to delete: ").strip()
            if not app_id.isdigit():
                print("ID must be a number.")
                pause()
                continue
            ok = tracker.delete(int(app_id))
            print("✅ Deleted." if ok else " ID not found.")
            pause()

        elif choice == "6":
            s = tracker.stats()
            print("\n=== Stats ===")
            print(f"Total applications: {s['total']}")
            for k, v in s["by_status"].items():
                print(f"{k}: {v}")
            print(f"Interview rate: {s['interview_rate_percent']}%")
            pause()
        elif choice == "7":
            keyword = input_non_empty("Enter company name keyword: ")
            results = tracker.search_company(keyword)
            print_applications(results)
            pause()


        elif choice == "0":
            print("Bye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
