import csv
from models.book import Book
from utils.logger import log_info, log_error


def save_books_to_file(books: list[Book], file_path: str):
    """
    Saves the list of books to a CSV file.
    Args:
        books (list[Book]): List of book objects to save.
        file_path (str): Path to the CSV file to save the books.
    """
    try:
        with open(file_path, "w", newline="") as file:
            fieldnames = ["id", "title", "author", "category", "year", "copies", "available"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for book in books:
                writer.writerow(book.to_dict())
        log_info(f"Books saved successfully to {file_path}.")
        print(f"Books saved successfully to {file_path}.")

    except Exception as e:
        print(f"Error saving books to file: {e}")
        log_error(f"Error saving books to file: {e}")


def load_books_from_file(file_path: str) -> list[Book]:
    """
    Loads the list of books from a CSV file.
    Args:
        file_path (str): Path to the CSV file to read the books.
    Returns:
        list[Book]: List of book objects read from the file.
    """
    books = []
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                book = Book(
                    id=int(row["id"]),
                    title=row["title"],
                    author=row["author"],
                    category=row["category"],
                    year=int(row["year"]),
                    copies=int(row["copies"]),
                )
                book.available = int(row["available"])
                books.append(book)

        print(f"Books loaded successfully from {file_path}.")
        log_info(f"Books loaded successfully from {file_path}.")
        return books

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        log_error(f"File {file_path} not found.")
        return []

    except Exception as e:
        print(f"Error loading books from file: {e}")
        return []
