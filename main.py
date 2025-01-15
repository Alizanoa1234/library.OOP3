import os
from services.library_manager import LibraryManager
from services.auth_manager import AuthManager
from utils.file_manager import load_books_from_file, save_books_to_file
from models.book import Book


def get_file_path(prompt, default):
    """
    Prompts the user for a file path or uses a default value.
    """
    file_path = input(f"{prompt} (default: {default}): ").strip()
    return file_path if file_path else default

def main():
    # Get file paths
    books_file_path = get_file_path("Enter path to books CSV", "data/books.csv")
    users_file_path = get_file_path("Enter path to users CSV", "data/users.csv")

    # Initialize managers
    library_manager = LibraryManager()
    auth_manager = AuthManager(users_file_path)

    # Load initial books
    library_manager.books = load_books_from_file(books_file_path)

    while True:
        print("""
--- Library System Menu ---
1. Register Librarian
2. Login Librarian
3. Add Book
4. Borrow Book
5. Return Book
6. Show Available Books
7. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":  # Register librarian
            username = input("Enter librarian username: ").strip()
            password = input("Enter librarian password: ").strip()
            auth_manager.register_librarian(username, password)

        elif choice == "2":  # Login
            username = input("Enter librarian username: ").strip()
            password = input("Enter librarian password: ").strip()
            auth_manager.login(username, password)

        elif choice == "3":  # Add book
            try:
                book_id = int(input("Enter book ID: "))
                title = input("Enter title: ")
                author = input("Enter author: ")
                category = input("Enter category: ")
                year = int(input("Enter year: "))
                copies = int(input("Enter number of copies: "))
                book = Book(book_id, title, author, category, year, copies)
                library_manager.add_book(book)
                save_books_to_file(library_manager.books, books_file_path)
            except ValueError:
                print("Invalid input. Please enter valid details.")

        elif choice == "4":  # Borrow book
            try:
                book_id = int(input("Enter book ID to borrow: "))
                library_manager.borrow_book(book_id)
            except ValueError:
                print("Invalid book ID.")

        elif choice == "5":  # Return book
            try:
                book_id = int(input("Enter book ID to return: "))
                library_manager.return_book(book_id)
            except ValueError:
                print("Invalid book ID.")

        elif choice == "6":  # Show available books
            library_manager.show_available_books()

        elif choice == "7":  # Exit
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")
