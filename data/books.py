import pandas as pd
from models.book import Book

def row_to_book(row: pd.Series) -> Book:
    """
    Convert a DataFrame row to a Book object.

    Args:
        row (pd.Series): A single row from the DataFrame.

    Returns:
        Book: A Book object created from the row data.
    """
    try:
        # Create and return the Book object
        book = Book(
            title=row["title"],
            author=row["author"],
            category=row["genre"],
            year=int(row["year"]),
            copies=int(row["copies"]),
            is_loaned_status=row["is_loaned"]  # Assuming it's already a dictionary
        )
        return book
    except KeyError as e:
        print(f"Missing key in the row: {e}")
    except Exception as e:
        print(f"Error converting row to Book: {e}")


def load_books_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Load books data from a CSV file, process the `is_loaned` column to store dictionaries
    mapping copy numbers to loan statuses, and return the updated DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The processed DataFrame with updated `is_loaned` column.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)

        # Standardize `is_loaned` to lowercase for consistency
        df['is_loaned'] = df['is_loaned'].str.lower()

        # Process `is_loaned` into a dictionary mapping copy numbers to statuses
        df['is_loaned'] = df.apply(
            lambda row: {i + 1: row['is_loaned'] for i in range(row['copies'])},
            axis=1
        )
        # Add `available` column based on the initial value of `is_loaned`
        df['available'] = df['is_loaned'].apply(
            lambda loaned_dict: any(status == 'no' for status in loaned_dict.values())
        )
        # Reorder columns to match the specified order
        column_order = ['title', 'author', 'copies', 'available', 'is_loaned', 'genre', 'year']
        df = df[column_order]

        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



def update_book_in_dataframe(df: pd.DataFrame, book: Book) -> pd.DataFrame:
    """
    Update a row in the DataFrame based on the data in the Book object.

    Args:
        df (pd.DataFrame): The DataFrame containing book data.
        book (Book): The Book object with updated data.

    Returns:
        pd.DataFrame: The updated DataFrame.
    """
    try:
        # Locate the row to update
        row_index = df[df['title'] == book.title].index[0]

        # Update the row with data from the Book object
        df.at[row_index, 'is_loaned'] = str(book.is_loaned)  # Convert dictionary to string
        df.at[row_index, 'available'] = book.available
        df.at[row_index, 'copies'] = book.copies
        df.at[row_index, 'borrow_count'] = book.borrow_count

        return df
    except IndexError:
        print(f"Error: Book '{book.title}' not found in the DataFrame.")
        return df
    except Exception as e:
        print(f"Error updating the DataFrame: {e}")
        return df
