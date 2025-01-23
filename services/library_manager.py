from data.books import load_books_from_file, save_books_to_file
from models.book import Book
from models.book_decorator import BookDecorator
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear
from services.auth_manager import AuthManager
from services.notification_manager import NotificationManager
from logs.actions import log_info, log_error
from data.users import User


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
        self.strategy = SearchByName()
        self.file_path = file_path
        self.books = load_books_from_file(self.file_path)
        self.decorators = {(book.title, book.author): BookDecorator(book) for book in self.books}
        auth_manager = AuthManager("data/users.csv")
        self.users = auth_manager.users_file
        self.notification_manager = NotificationManager(self.users)

    def add_book(self, book: Book, additional_copies: int = 0) -> bool:
        for existing_book in self.books:
            if existing_book.title == book.title and existing_book.author == book.author:
                existing_book.copies += additional_copies
                existing_book.available += additional_copies
                for i in range(existing_book.copies - additional_copies + 1, existing_book.copies + 1):
                    existing_book.is_loaned[i] = 'no'

                if existing_book.available > existing_book.copies:
                    log_error(f"Inconsistent state for book '{existing_book.title}' by {existing_book.author}.")
                    existing_book.available = existing_book.copies

                save_books_to_file(self.file_path)

                log_info(f"Added {additional_copies} copies to '{existing_book.title}' by {existing_book.author}.")
                self.notification_manager.notify_all(
                    f"{additional_copies} additional copies of '{existing_book.title}' by {existing_book.author} are now available."
                )
                return True

        book.is_loaned = {i + 1: 'no' for i in range(book.copies)}
        book.available = book.copies
        book.borrow_count = 0
        book.popularity_score = book.borrow_count + len(book.waiting_list)
        book.waiting_list = []
        self.books.append(book)

        self.decorators[(book.title, book.author)] = BookDecorator(book)
        save_books_to_file(self.file_path)
        log_info(f"New book '{book.title}' by {book.author} added successfully.")
        self.notification_manager.notify_all(f"New book added: '{book.title}' by {book.author}")
        return True

    def remove_book(self, title: str, author: str) -> bool:
        for book in self.books:
            if book.title == title and book.author == author:
                if book.available < book.copies:
                    log_error(f"Cannot remove book '{title}' by {author} as it has borrowed copies.")
                    return False

                self.books.remove(book)
                del self.decorators[(title, author)]
                save_books_to_file(self.file_path)
                log_info(f"Book '{title}' by {author} removed successfully.")
                self.notification_manager.notify_all(f"Book '{title}' by {author} has been removed.")
                return True

        log_error(f"Book '{title}' by {author} not found.")
        return False

    def borrow_book(self, title: str, author: str, user_id: str) -> bool:
        for book in self.books:
            if book.title == title and book.author == author:
                if book.available > 0:
                    for copy_id, status in book.is_loaned.items():
                        if status == 'no':
                            book.is_loaned[copy_id] = 'yes'
                            book.available -= 1
                            book.borrow_count += 1
                            save_books_to_file(self.file_path)
                            log_info(f"Book '{title}' borrowed successfully. Copy ID: {copy_id}")
                            return True

                if user_id not in book.waiting_list:
                    book.waiting_list.append(user_id)
                    log_info(f"User {user_id} added to waiting list for '{title}'.")
                    self.notification_manager.notify_all(f"Book '{title}' by {author} is currently unavailable.")
                return False

        log_error(f"Book '{title}' by {author} not found in the library.")
        return False

    def return_book(self, title: str, author: str) -> bool:
        for book in self.books:
            if book.title == title and book.author == author:
                for copy_id, status in book.is_loaned.items():
                    if status == 'yes':  # Find the first loaned copy
                        book.is_loaned[copy_id] = 'no'
                        book.available += 1
                        save_books_to_file(self.file_path)
                        log_info(f"Book '{title}' returned successfully. Copy ID: {copy_id}")

                        # Handle waiting list
                        if book.waiting_list:
                            next_user = book.waiting_list.pop(0)
                            log_info(f"User {next_user} notified for book '{title}'.")
                            self.notification_manager.notify_user(next_user, f"Book '{title}' is now available.")
                        return True

        log_error(f"Book '{title}' by {author} not found in the library.")
        return False
