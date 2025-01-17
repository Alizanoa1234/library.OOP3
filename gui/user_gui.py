from services.auth_manager import AuthManager

auth_manager = AuthManager("data/users.csv")

def user_login():
    """
    Displays the user login and registration menu.
    """
    while True:
        print("""
--- User Management ---
1. Register
2. Login
3. Back to Main Menu
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def register_user():
    """
    Registers a new user.
    """
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    auth_manager.register_librarian(username, password)

def login_user():
    """
    Logs in an existing user.
    """
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    auth_manager.login(username, password)
