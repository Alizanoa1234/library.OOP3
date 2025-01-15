from models.book import Book
from services.observer import Subscriber, ObserverManager
from services.library_manager import LibraryManager


def main():
    library_manager = LibraryManager()

    # Sample books
    book1 = Book(1, "Clean Code", "Robert C. Martin", "Programming", 2008, 2)
    book2 = Book(2, "The Pragmatic Programmer", "Andy Hunt", "Programming", 1999, 1)

    # Add sample books to the library
    library_manager.add_book(book1)
    library_manager.add_book(book2)

    while True:
        print("\n--- Library System Menu ---")
        print("1. Add subscriber to waitlist")
        print("2. Remove subscriber from waitlist")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Show available books")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            book_id = int(input("Enter book ID to subscribe: "))
            librarian_name = input("Enter librarian's name: ")
            librarian_email = input("Enter librarian's email: ")
            library_manager.add_subscriber_to_book(book_id, librarian_name, librarian_email)

        elif choice == "2":
            book_id = int(input("Enter book ID to remove subscriber: "))
            librarian_email = input("Enter librarian's email to remove: ")
            library_manager.remove_subscriber_from_book(book_id, librarian_email)

        elif choice == "3":
            book_id = int(input("Enter book ID to borrow: "))
            success = library_manager.borrow_book(book_id)
            if success:
                print("Borrowed successfully!")
            else:
                print("Borrowing failed. No copies available or invalid book ID.")

        elif choice == "4":
            book_id = int(input("Enter book ID to return: "))
            success = library_manager.return_book(book_id)
            if success:
                print("Returned successfully!")
            else:
                print("Returning failed. Invalid book ID.")

        elif choice == "5":
            library_manager.show_available_books()

        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
