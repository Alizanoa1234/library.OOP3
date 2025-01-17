import sys
from gui.books_gui import manage_books
from gui.search_gui import search_books
from gui.user_gui import user_login

def main_menu():
    """
    Displays the main menu and navigates to different functionalities.
    """
    while True:
        print("""
--- Library Management System ---
1. Manage Books
2. Search Books
3. User Login
4. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            manage_books()
        elif choice == "2":
            search_books()
        elif choice == "3":
            user_login()
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
