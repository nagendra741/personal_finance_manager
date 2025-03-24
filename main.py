from auth.authentication import register_user, login_user
from transactions.income import add_income, view_income
from transactions.expense import add_expense, view_expense  # Ensure this function exists
from reports.report_generator import generate_report
from budget.budget_tracker import set_budget, check_budget
from backup.backup_restore import backup_database, restore_database


def user_dashboard(username):
    while True:
        print("\n Welcome to Personal Finance Manager!")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Income")
        print("4. View Expenses")
        print("5. Generate Financial Report")
        print("6. Set Budget")
        print("7. Check Budget")
        print("8. Backup Data")
        print("9. Restore Data")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter income amount: "))
            category = input("Enter category: ")
            add_income(username, amount, category)
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            category = input("Enter category: ")
            add_expense(username, amount, category)
        elif choice == "3":
            view_income(username)
        elif choice == "4":
            view_expense(username)
        elif choice == "5":
            generate_report(username)
        elif choice == "6":
            category = input("Enter category: ")
            limit = float(input("Enter budget limit: "))
            set_budget(username, category, limit)
        elif choice == "7":
            check_budget(username)
        elif choice == "8":
            backup_database()
        elif choice == "9":
            restore_database()
        elif choice == "10":
            print(" Logged out successfully!")
            break
        else:
            print(" Invalid option! Try again.")

def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password):
                user_dashboard(username)  # Show the full dashboard after login
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print(" Invalid option! Try again.")

if __name__ == "__main__":
    main()
