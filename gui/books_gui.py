from models.book import Book
from services.library_manager import LibraryManager
from data.users import UsersManager  # Import UsersManager

# Initialize UsersManager
users_manager = UsersManager()

# Load the users file for NotificationManager compatibility
users_file = users_manager.USERS_FILE

# Initialize LibraryManager with the required file paths
library_manager = LibraryManager("data/books.csv")

def manage_books():
    """
    Displays the book management menu.
    """
    while True:
        print("""
--- Manage Books ---
1. Add Book
2. Remove Book
3. Borrow Book
4. Return Book
5. Show Available Books
6. Back to Main Menu
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_available_books()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def add_book():
    """
    Adds a new book or increases copies of an existing book.
    """
    try:
        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()
        category = input("Enter category: ").strip()
        year = int(input("Enter year: ").strip())
        copies = int(input("Enter number of copies: ").strip())
        book = Book(title, author, category, year, copies)
        if library_manager.add_book(book, additional_copies=copies):
            print(f"Book '{title}' by {author} added/updated successfully.")
        else:
            print(f"Failed to add/update book '{title}' by {author}.")
    except ValueError:
        print("Invalid input. Please enter valid details.")

def remove_book():
    """
    Removes a book from the library.
    """
    title = input("Enter book title to remove: ").strip()
    author = input("Enter author: ").strip()
    if library_manager.remove_book(title, author):
        print(f"Book '{title}' by {author} removed successfully.")
    else:
        print(f"Failed to remove book '{title}' by {author}.")

def borrow_book():
    """
    Borrows a book if available.
    """
    title = input("Enter book title to borrow: ").strip()
    author = input("Enter author: ").strip()
    if library_manager.borrow_book(title, author):
        print(f"Book '{title}' borrowed successfully.")
    else:
        print(f"Book '{title}' is unavailable or not found.")

def return_book():
    """
    Returns a borrowed book.
    """
    title = input("Enter book title to return: ").strip()
    author = input("Enter author: ").strip()
    if library_manager.return_book(title, author):
        print(f"Book '{title}' returned successfully.")
    else:
        print(f"Failed to return book '{title}' by {author}.")

def show_available_books():
    """
    Displays all books with their available copies.
    """
    print("\n--- Available Books ---")
    library_manager.show_available_books()
    print("-----------------------")
