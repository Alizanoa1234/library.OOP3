import csv
from models.book import Book


class FileStorageManager:
    """
    Manages data storage using a CSV file.
    Responsible for reading and writing the book list to a file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the storage manager with the file path.

        Args:
            file_path (str): Path to the storage file.
        """
        self.file_path = file_path

    def load_books(self) -> list[Book]:
        """
        Loads a list of books from a CSV file.

        Returns:
            list[Book]: A list of Book objects.
        """
        books = []
        try:
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        id=int(row["id"]),
                        title=row["title"],
                        author=row["author"],
                        category=row["category"],
                        year=int(row["year"]),
                        copies=int(row["copies"])
                    )
                    books.append(book)
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
        except Exception as e:
            print(f"Error loading books: {e}")
        return books

    def save_books(self, books: list[Book]):
        """
        Saves a list of books to a CSV file.

        Args:
            books (list[Book]): List of books to save.
        """
        try:
            with open(self.file_path, "w", newline="") as file:
                fieldnames = ["id", "title", "author", "category", "year", "copies"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in books:
                    writer.writerow({
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "category": book.category,
                        "year": book.year,
                        "copies": book.copies
                    })
        except Exception as e:
            print(f"Error saving books: {e}")
