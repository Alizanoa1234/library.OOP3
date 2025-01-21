from data.books import load_books_from_file, save_books_to_file
from models.book import Book
from models.book_decorator import BookDecorator
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear
from services.notification_manager import NotificationManager
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
        self.decorators = {(book.title, book.author): BookDecorator(book) for book in self.books}  # Decorate books
        self.search_manager = SearchManager(SearchByName())  # Default search strategy is by title
        self.notification_manager = NotificationManager()

    def add_book(self, book: Book, additional_copies: int = 0) -> bool:
        """
        Adds a new book to the library or increases the number of copies if the book already exists.

        Args:
            book (Book): The book to add.
            additional_copies (int): Additional copies to add to an existing book.

        Returns:
            bool: True if the book was added or updated, False otherwise.
        """
        for existing_book in self.books:
            if existing_book.title == book.title and existing_book.author == book.author:
                existing_book.copies += additional_copies
                existing_book.available += additional_copies
                save_books_to_file(self.file_path)
                log_info(f"Added {additional_copies} copies to '{existing_book.title}' by {existing_book.author}.")
                self.notification_manager.notify_all(
                    f"{additional_copies} additional copies of '{existing_book.title}' by {existing_book.author} are now available."
                )
                return True

        self.books.append(book)
        self.decorators[(book.title, book.author)] = BookDecorator(book)
        save_books_to_file(self.file_path)
        log_info(f"New book '{book.title}' by {book.author} added successfully.")
        self.notification_manager.notify_all(f"New book added: '{book.title}' by {book.author}")
        return True

    def remove_book(self, title: str, author: str) -> bool:
        """
        Removes a book from the library.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.

        Returns:
            bool: True if the book was successfully removed, False otherwise.
        """
        for book in self.books:
            if book.title == title and book.author == author:
                self.books.remove(book)
                del self.decorators[(title, author)]
                save_books_to_file(self.books, self.file_path)
                log_info(f"Book '{title}' by {author} removed successfully.")
                self.notification_manager.notify_all(f"Book '{title}' by {author} has been removed.")
                return True

        log_error(f"Book '{title}' by {author} not found.")
        return False

    def borrow_book(self, title: str, author: str) -> bool:
        """
        Borrows a book by title and author if copies are available.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.

        Returns:
            bool: True if the book was successfully borrowed, False otherwise.
        """
        for book in self.books:
            if book.title == title and book.author == author:
                if book.available > 0:
                    book.available -= 1
                    book.borrow_count += 1
                    save_books_to_file(self.file_path)
                    log_info(f"Book '{title}' borrowed successfully.")
                    return True
                else:
                    log_info(f"No available copies for book '{title}'. Adding to waiting list.")
                    self.notification_manager.notify_all(f"Book '{title}' by {author} is currently unavailable.")
                    return False

        log_error(f"Book '{title}' by {author} not found in the library.")
        return False

    def return_book(self, title: str, author: str) -> bool:
        """
        Returns a borrowed book by title and author.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.

        Returns:
            bool: True if the book was successfully returned, False otherwise.
        """
        for book in self.books:
            if book.title == title and book.author == author:
                book.available += 1
                save_books_to_file(self.books, self.file_path)
                log_info(f"Book '{title}' returned successfully.")
                self.notification_manager.notify_all(f"Book '{title}' by {author} is now available.")
                return True

        log_error(f"Book '{title}' by {author} not found in the library.")
        return False

    def show_available_books(self):
        """
        Displays all books with their available copies.
        """
        log_info("Displaying all available books:")
        for book in self.books:
            print(f"{book.title} by {book.author} - Available copies: {book.available}")
