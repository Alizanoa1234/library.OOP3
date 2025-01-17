import pandas as pd
from models.book import Book

def load_books_from_file(file_path: str) -> list:
    """
    Loads books from the original CSV file and initializes them as Book objects.

    Args:
        file_path (str): Path to the original file.

    Returns:
        list: List of Book objects.
    """
    books = []
    try:
        # Load CSV into a Pandas DataFrame
        df = pd.read_csv(file_path)

        # Iterate over rows and create Book objects
        for _, row in df.iterrows():
            book = Book(
                title=row["title"],
                author=row["author"],
                category=row["genre"],
                year=int(row["year"]),
                copies=int(row["copies"]),
                is_loaned_status=row["is_loaned"].strip().lower()  # Pass the loan status directly
            )
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
        # Create a list of dictionaries to save in the DataFrame
        data = []
        for book in books:
            data.append({
                "title": book.title,
                "author": book.author,
                "is_loaned": str(book.is_loaned),  # Convert dictionary to string
                "copies": book.copies,
                "genre": book.category,
                "year": book.year,
                "available": book.available,
                "borrow_count": book.borrow_count,
            })

        # Create a DataFrame and save to CSV
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    except Exception as e:
        print(f"Error saving books: {e}")
