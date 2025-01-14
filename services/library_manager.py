from models.book import Book
from models.book_decorator import BookDecorator
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear


class LibraryManager:
    """
    Manages the library's books, borrowing process, and popular books.
    """

    def __init__(self):
        """
        Initializes the LibraryManager with an empty list of books and a dictionary of decorated books.
        """
        self.books = []  # List of books
        self.decorators = {}  # Maps book ID to its decorated version
        self.search_manager = SearchManager(SearchByName())  # Default search strategy is by title

    def add_book(self, book: Book):
        """
        Adds a new book to the library and wraps it with a decorator.

        Args:
            book (Book): The book to add.
        """
        if any(b.id == book.id for b in self.books):
            print(f"Book with ID {book.id} already exists.")
            return False

        self.books.append(book)
        self.decorators[book.id] = BookDecorator(book)
        print(f"Book '{book.title}' added successfully.")
        return True

    def remove_book(self, book_id: int) -> bool:
        """
        Removes a book from the library by its ID.

        Args:
            book_id (int): The ID of the book to remove.

        Returns:
            bool: True if the book was successfully removed, False otherwise.
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                del self.decorators[book_id]
                print(f"Book '{book.title}' removed successfully.")
                return True
        print(f"Book with ID {book_id} not found.")
        return False

    def borrow_book(self, book_id: int) -> bool:
        """
        Borrows a book and updates its borrow count.

        Args:
            book_id (int): The ID of the book to borrow.

        Returns:
            bool: True if the book was successfully borrowed, False otherwise.
        """
        for book in self.books:
            if book.id == book_id and book.is_available():
                book.update_copies(-1)
                self.decorators[book_id].increase_borrow_count()  # Track borrow count
                print(f"Book '{book.title}' borrowed successfully.")
                return True
        print("Book is not available for borrowing.")
        return False

    def return_book(self, book_id: int) -> bool:
        """
        Returns a borrowed book and updates its availability.

        Args:
            book_id (int): The ID of the book to return.

        Returns:
            bool: True if the book was successfully returned, False otherwise.
        """
        for book in self.books:
            if book.id == book_id:
                book.update_copies(1)
                print(f"Book '{book.title}' returned successfully.")
                return True
        print(f"Book with ID {book_id} not found.")
        return False

    def get_popular_books(self, top_n: int = 10) -> list:
        """
        Returns the top N most popular books based on borrow count.

        Args:
            top_n (int): The number of top books to return. Default is 10.

        Returns:
            list: A list of the most popular books, sorted by borrow count.
        """
        sorted_books = sorted(
            self.decorators.values(),
            key=lambda decorator: decorator.get_borrow_count(),
            reverse=True,
        )
        return sorted_books[:top_n]

    def search_books(self, query: str, search_by: str = "title"):
        """
        Searches for books using a specific search strategy.

        Args:
            query (str): The search query.
            search_by (str): The search type (title, author, or category).

        Returns:
            list: A list of books matching the search query.
        """
        if search_by == "title":
            self.search_manager.set_strategy(SearchByName())
        elif search_by == "author":
            self.search_manager.set_strategy(SearchByAuthor())
        elif search_by == "category":
            self.search_manager.set_strategy(SearchByCategory())
        elif search_by == "year":
            self.search_manager.set_strategy(SearchByYear())
        else:
            raise ValueError(f"Invalid search type: {search_by}")

        return self.search_manager.search(self.books, query)

    def set_search_strategy(self, strategy: str):
        if strategy == "title":
            self.search_manager.set_strategy(SearchByName())
        elif strategy == "author":
            self.search_manager.set_strategy(SearchByAuthor())
        elif strategy == "category":
            self.search_manager.set_strategy(SearchByCategory())
        else:
            raise ValueError(f"Unknown search strategy: {strategy}")


