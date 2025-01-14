class Book:
    """
    Represents a book in the library system.
   """

    def __init__(
            self, id: int, title: str, author: str, category: str, year: int, copies: int
    ):
        """
       Initializes a new book with its details.

       Args:
           id (int): Unique identifier.
           title (str): Title of the book.
           author (str): Author's name.
           category (str): Book's category.
           year (int): Publication year.
           copies (int): Total copies in the library.
       """
        if copies < 0:
            raise ValueError("Number of copies cannot be negative.")
        if not title or not author or not category:
            raise ValueError("Title, author, and category cannot be empty.")

        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.year = year
        self.copies = copies
        self.available = copies


def update_copies(self, delta: int):
    """
    Updates the number of available copies.
   """
    if self.available + delta < 0:
        raise ValueError("Available copies cannot be negative.")
    self.available += delta


def is_available(self) -> bool:
    """
    Checks if the book is available for lending.
    """
    return self.available > 0


def __str__(self) -> str:
    """
    Returns a string representation of the book.
    """
    return (f"Book[ID={self.id}, Title={self.title}, Author={self.author},"
            f" Category={self.category}, Year={self.year}, Copies={self.copies}, Available={self.available}]")


def to_dict(self) -> dict:
    """
    Converts the book's attributes to a dictionary.
    """
    return {
        "id": self.id,
        "title": self.title,
        "author": self.author,
        "category": self.category,
        "year": self.year,
        "copies": self.copies,
        "available": self.available,
    }


def __lt__(self, other: object) -> bool:
    """
    Compares books by publication year.
    """
    if not isinstance(other, Book):
        return NotImplemented
    return self.year < other.year

