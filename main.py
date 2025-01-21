import pandas as pd
from werkzeug.security import generate_password_hash

from data.users import UsersManager


def main():
    """
    Main function to manage librarian users in the library system.
    Provides a CLI for managing librarians with additional functionality.
    """
    users_manager = UsersManager()

    while True:
        print("""
--- Library User Management ---
1. Register Librarian
2. Check if Librarian Exists
3. Authenticate Librarian
4. View All Librarians
5. Delete Librarian
6. Update Librarian Password
7. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_librarian(users_manager)
        elif choice == "2":
            check_librarian(users_manager)
        elif choice == "3":
            authenticate_librarian(users_manager)
        elif choice == "4":
            view_all_librarians(users_manager)
        elif choice == "5":
            delete_librarian(users_manager)
        elif choice == "6":
            update_librarian_password(users_manager)
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def register_librarian(users_manager):
    """
    Registers a new librarian.

    Args:
        users_manager (UsersManager): Instance of UsersManager.
    """
    while True:
        username = input("Enter librarian username (at least 5 characters): ").strip()
        if len(username) < 5:
            print("Username must be at least 5 characters long. Try again.")
            continue
        password = input("Enter librarian password (at least 8 characters): ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters long. Try again.")
            continue
        success, message = users_manager.register_librarian(username, password)
        print(message)
        break


def check_librarian(users_manager):
    """
    Checks if a librarian exists.

    Args:
        users_manager (UsersManager): Instance of UsersManager.
    """
    username = input("Enter librarian username to check: ").strip()
    if users_manager.is_librarian_exists(username):
        print(f"Librarian '{username}' exists.")
    else:
        print(f"Librarian '{username}' does not exist.")


def authenticate_librarian(users_manager):
    """
    Authenticates a librarian.

    Args:
        users_manager (UsersManager): Instance of UsersManager.
    """
    username = input("Enter librarian username: ").strip()
    password = input("Enter librarian password: ").strip()
    if users_manager.authenticate_librarian(username, password):
        print(f"Librarian '{username}' authenticated successfully.")
    else:
        print("Authentication failed. Please check your username or password.")


def view_all_librarians(users_manager):
    """
    Displays all registered librarians.
    """
    try:
        df = pd.read_csv(users_manager.USERS_FILE)
        if df.empty:
            print("No librarians are registered yet.")
        else:
            print("\n--- Registered Librarians ---")
            print(df[['username']].to_string(index=False))
            print("----------------------------")
    except FileNotFoundError:
        print("No users file found. Please register a librarian first.")


def delete_librarian(users_manager):
    """
    Deletes a librarian from the system.

    Args:
        users_manager (UsersManager): Instance of UsersManager.
    """
    username = input("Enter librarian username to delete: ").strip()
    if not users_manager.is_librarian_exists(username):
        print(f"Librarian '{username}' does not exist.")
        return

    try:
        df = pd.read_csv(users_manager.USERS_FILE)
        df = df[df['username'] != username]
        df.to_csv(users_manager.USERS_FILE, index=False)
        print(f"Librarian '{username}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting librarian: {e}")


def update_librarian_password(users_manager):
    """
    Updates a librarian's password.

    Args:
        users_manager (UsersManager): Instance of UsersManager.
    """
    username = input("Enter librarian username: ").strip()
    if not users_manager.is_librarian_exists(username):
        print(f"Librarian '{username}' does not exist.")
        return

    old_password = input("Enter current password: ").strip()
    if not users_manager.authenticate_librarian(username, old_password):
        print("Incorrect current password.")
        return

    new_password = input("Enter new password (at least 8 characters): ").strip()
    if len(new_password) < 8:
        print("New password must be at least 8 characters long. Try again.")
        return

    try:
        df = pd.read_csv(users_manager.USERS_FILE)
        df.loc[df['username'] == username, 'password'] = generate_password_hash(new_password)
        df.to_csv(users_manager.USERS_FILE, index=False)
        print("Password updated successfully.")
    except Exception as e:
        print(f"Error updating password: {e}")


if __name__ == "__main__":
    main()

