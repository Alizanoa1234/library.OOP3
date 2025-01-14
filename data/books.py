import csv
from models.book import Book

def load_books_from_file(file_path: str) -> list:
    """
    Loads books from the original CSV file and initializes the is_loaned field as a dictionary.

    Args:
        file_path (str): Path to the original file.

    Returns:
        list: List of Book objects with dynamic is_loaned fields.
    """
    books = []
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(
                    id=None,  # אין מזהה ייחודי בקובץ המקורי
                    title=row["title"],
                    author=row["author"],
                    category=row["genre"],
                    year=int(row["year"]),
                    copies=int(row["copies"]),
                )
                # יצירת מילון עבור is_loaned לפי מספר העותקים
                is_loaned = row["is_loaned"].strip().lower() == "yes"
                book.is_loaned = {i: "yes" if is_loaned else "no" for i in range(book.copies)}

                # השדות הדינמיים הנוספים
                book.available = book.copies - sum(1 for status in book.is_loaned.values() if status == "yes")
                book.borrow_count = 0
                books.append(book)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error loading books: {e}")
    return books


def save_books_to_file(books: list, file_path: str):
    """
    Saves books to a new CSV file, including the is_loaned field as a dictionary.

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



def create_working_copy(original_file: str, working_copy: str):
    """
    Creates a working copy of the original CSV file.

    Args:
        original_file (str): Path to the original file.
        working_copy (str): Path to the working copy.
    """
    import shutil
    try:
        shutil.copy(original_file, working_copy)
        print(f"Working copy created at {working_copy}.")
    except Exception as e:
        print(f"Error creating working copy: {e}")


def borrow_book(self, book_id: int) -> bool:
    for book in self.books:
        if book.id == book_id:
            for copy_id, status in book.is_loaned.items():
                if status == "no":
                    book.is_loaned[copy_id] = "yes"
                    book.available -= 1
                    book.borrow_count += 1
                    save_books_to_file(self.books, "books_working_copy.csv")
                    return True
    print("No available copies to borrow.")
    return False


def return_book(self, book_id: int, copy_id: int) -> bool:
    for book in self.books:
        if book.id == book_id and book.is_loaned.get(copy_id) == "yes":
            book.is_loaned[copy_id] = "no"
            book.available += 1
            save_books_to_file(self.books, "books_working_copy.csv")
            return True
    print("Invalid book ID or copy ID.")
    return False


  def has_available_copies(self) -> bool:
        """
        Checks if there are available copies for this book.

        Returns:
            bool: True if at least one copy is not loaned, False otherwise.
        """
        return any(status == "no" for status in self.is_loaned.values())
