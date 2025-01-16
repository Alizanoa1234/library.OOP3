import csv
from models.book import Book

def load_books_from_file(file_path: str) -> list:
    """
    Loads books from the original CSV file and initializes them as Book objects,
    setting the correct loan status for each copy based on the data in the CSV file.

    Args:
        file_path (str): Path to the original file.

    Returns:
        list: List of Book objects.
    """
    books = []
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(
                    title=row["title"],
                    author=row["author"],
                    category=row["genre"],
                    year=int(row["year"]),
                    copies=int(row["copies"])
                )

                # Initialize the is_loaned dictionary based on the CSV data
                is_loaned_status = row["is_loaned"].strip().lower()  # "yes" or "no"
                for i in range(book.copies):
                    book.is_loaned[i] = is_loaned_status  # Set all copies to the same loan status

                # Update availability count based on loan status
                if is_loaned_status == "yes":
                    book.available = 0
                else:
                    book.available = book.copies  # All copies are available if not loaned

                books.append(book)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error loading books: {e}")
    return books


def save_books_to_file(books: list, file_path: str):
    """
    Saves books to a new CSV file, including the is_loaned field.

    Args:
        books (list): List of Book objects.
        file_path (str): Path to the CSV file.
    """
    try:
        with open(file_path, "w", newline="") as file:
            fieldnames = ["title", "author", "is_loaned", "copies", "genre", "year", "available", "borrow_count"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow({
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": str(book.is_loaned),  # המרת המילון למחרוזת
                    "copies": book.copies,
                    "genre": book.category,
                    "year": book.year,
                    "available": book.available,
                    "borrow_count": book.borrow_count,
                })
    except Exception as e:
        print(f"Error saving books: {e}")
