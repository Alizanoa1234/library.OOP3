from models.book import Book
from services.library_manager import LibraryManager

library_manager = LibraryManager("data/books.csv", [])

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
5. Back to Main Menu
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
        library_manager.add_book(book, additional_copies=copies)
    except ValueError:
        print("Invalid input. Please enter valid details.")

def remove_book():
    """
    Removes a book from the library.
    """
    title = input("Enter book title to remove: ").strip()
    author = input("Enter author: ").strip()
    for book in library_manager.books:
        if book.title == title and book.author == author:
            library_manager.remove_book(book)
            return
    print("Book not found.")

def borrow_book():
    """
    Borrows a book if available.
    """
    title = input("Enter book title to borrow: ").strip()
    author = input("Enter author: ").strip()
    for book in library_manager.books:
        if book.title == title and book.author == author:
            library_manager.borrow_book(book)
            return
    print("Book not found or unavailable.")


def return_book():
    """
    Returns a borrowed book.
    """
    title = input("Enter book title to return: ").strip()
    author = input("Enter author: ").strip()
    for book in library_manager.books:
        if book.title == title and book.author == author:
            library_manager.return_book(book)
            return
    print("Book not found.")
