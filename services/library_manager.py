from data.books import load_books_from_file, save_books_to_file
from models.book import Book
from models.book_decorator import BookDecorator
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear
from services.notification_manager import  NotificationManager
from logs.actions import log_info, log_error


class LibraryManager:
    """
    Manages the library's books, borrowing process, and popular books.
    """

    def __init__(self, file_path: str):
        """
        Initializes the LibraryManager with books loaded from the specified CSV file.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path  # Path to the original books.csv file
        self.books = load_books_from_file(self.file_path)  # Load books from the original CSV
        self.decorators = {book: BookDecorator(book) for book in self.books}  # Decorate books
        self.search_manager = SearchManager(SearchByName())  # Default search strategy is by title
        self.notification_manager = NotificationManager()

    def add_book(self, book: Book, additional_copies: int = 0):
        """
        Adds a new book to the library or increases the number of copies if the book already exists.

        Args:
            book (Book): The book to add.
            additional_copies (int): Additional copies to add to an existing book.
        """
        for existing_book in self.books:
            if existing_book.title == book.title and existing_book.author == book.author:
                # Update copies for an existing book
                existing_book.copies += additional_copies
                existing_book.available += additional_copies
                save_books_to_file(self.books, self.file_path)
                log_info(f"Added {additional_copies} copies to '{existing_book.title}' by {existing_book.author}.")
                self.notification_manager.notify_all(
                    f"{additional_copies} additional copies of '{existing_book.title}' by {existing_book.author} are now available."
                )
                return True

        # Add new book if it doesn't exist
        self.books.append(book)
        self.decorators[book] = BookDecorator(book)
        save_books_to_file(self.books, self.file_path)
        log_info(f"New book '{book.title}' by {book.author} added successfully.")
        self.notification_manager.notify_all(f"New book added: '{book.title}' by {book.author}")
        return True

    def remove_book(self, book: Book) -> bool:
        """
        Removes a book from the library.

        Args:
            book (Book): The book to remove.

        Returns:
            bool: True if the book was successfully removed, False otherwise.
        """
        if book in self.books:
            self.books.remove(book)
            del self.decorators[book]
            save_books_to_file(self.books, self.file_path)
            log_info(f"Book '{book.title}' removed successfully.")
            self.notification_manager.notify_all(f"Book '{book.title}' by {book.author} has been removed.")
            return True

        log_error(f"Book '{book.title}' by {book.author} not found.")
        return False

    def borrow_book(self, book: Book) -> bool:
        """
        Borrows a book if copies are available or puts the request on the waiting list.

        Args:
            book (Book): The book to borrow.

        Returns:
            bool: True if the book was successfully borrowed, False otherwise.
        """
        if book not in self.books:
            log_error(f"Book '{book.title}' by {book.author} not found in the library.")
            return False

        if book.available > 0:
            book.available -= 1
            book.borrow_count += 1
            save_books_to_file(self.books, self.file_path)
            log_info(f"Book '{book.title}' borrowed successfully.")
            return True
        else:
            log_info(f"No available copies for book '{book.title}'. Adding to waiting list.")
            self.notification_manager.notify_all(f"Book '{book.title}' by {book.author} is currently unavailable. You've been added to the waiting list.")
            return False

    def return_book(self, book: Book) -> bool:
        """
        Returns a borrowed book and notifies the waiting list.

        Args:
            book (Book): The book to return.

        Returns:
            bool: True if the book was successfully returned, False otherwise.
        """
        if book not in self.books:
            log_error(f"Book '{book.title}' by {book.author} not found in the library.")
            return False

        book.available += 1
        save_books_to_file(self.books, self.file_path)
        log_info(f"Book '{book.title}' returned successfully.")
        self.notification_manager.notify_all(f"Book '{book.title}' by {book.author} is now available. Check it out soon!")
        return True

    def show_available_books(self):
        """
        Displays all books with their available copies.
        """
        log_info("Displaying all available books:")
        for book in self.books:
            print(f"{book.title} by {book.author} - Available copies: {book.available}")
