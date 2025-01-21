import pandas as pd
from models.book import Book
from data import dataManager  # Import the DataManager

def load_books_to_dataframe(file_path: str) -> None:
    """
    Load books data from a CSV file, process the `is_loaned` column to store dictionaries
    mapping copy numbers to loan statuses, and initialize the DataFrame in DataManager.

    Args:
        file_path (str): Path to the CSV file.
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
            lambda loaned_dict: sum(1 for status in loaned_dict.values() if status == 'no')
        )

        # Add an empty `waiting_list` column if it doesn't exist
        if 'waiting_list' not in df.columns:
            df['waiting_list'] = [[] for _ in range(len(df))]

        # Reorder columns to match the specified order
        column_order = ['title', 'author', 'copies', 'available', 'is_loaned', 'waiting_list', 'genre', 'year']
        df = df[column_order]

        # Initialize the DataManager with the DataFrame
        data_manager = dataManager.get_instance()
        data_manager.initialize_data(df)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


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


def update_book_in_dataframe(book: Book) -> None:
    """
    Update a row in the DataFrame managed by DataManager based on the data in the Book object.

    Args:
        book (Book): The Book object with updated data.
    """
    try:
        # Get the DataFrame from DataManager
        data_manager = dataManager.get_instance()
        df = data_manager.get_data()

        # Locate the row to update
        row_index = df[df['title'] == book.title].index[0]

        # Update the row with data from the Book object
        df.at[row_index, 'is_loaned'] = book.is_loaned  # Keep it as a dictionary
        df.at[row_index, 'available'] = book.available
        df.at[row_index, 'copies'] = book.copies
        df.at[row_index, 'waiting_list'] = book.waiting_list

    except IndexError:
        print(f"Error: Book '{book.title}' not found in the DataFrame.")
    except Exception as e:
        print(f"Error updating the DataFrame: {e}")


def save_updated_dataframe(file_path: str) -> None:
    """
    Save the updated DataFrame managed by DataManager to a file.

    Args:
        file_path (str): The path to the file where the DataFrame should be saved.
    """
    try:
        # Get the DataFrame from DataManager
        data_manager = DataManager.get_instance()
        df = data_manager.get_data()

        # Save the entire DataFrame to the file
        df.to_csv(file_path, index=False)
        print(f"All updated data successfully saved to {file_path}.")
    except Exception as e:
        print(f"Error saving the updated DataFrame: {e}")
