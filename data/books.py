import pandas as pd
from models.book import Book

class DataManager:
    _instance = None

    @staticmethod
    def get_instance():
        if DataManager._instance is None:
            DataManager()
        return DataManager._instance

    def __init__(self):
        if DataManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.data = None
            DataManager._instance = self

    def initialize_data(self, dataframe):
        self.data = dataframe

    def get_data(self):
        return self.data

def load_books_from_file(file_path="books.csv"):
    """Load books from a CSV file into a DataFrame and initialize the DataManager."""
    try:
        books_df = pd.read_csv(file_path)

        # Standardize `is_loaned` to lowercase for consistency
        books_df['is_loaned'] = books_df['is_loaned'].apply(eval)

        # Add `available` column based on `is_loaned`
        books_df['available'] = books_df['is_loaned'].apply(
            lambda loaned_dict: sum(1 for status in loaned_dict.values() if status == 'no')
        )
        books_df['borrow_count'] = books_df['copies'] - books_df['available']

        # Calculate the size of the waiting list for each book
        books_df['popularity_score'] = books_df['borrow_count'] + books_df['waiting_list'].apply(len)

        # Add an empty `waiting_list` column if it doesn't exist
        if 'waiting_list' not in books_df.columns:
            books_df['waiting_list'] = [[] for _ in range(len(books_df))]

        # Reorder columns for consistency
        column_order = ['title', 'author', 'copies', 'available', 'is_loaned', 'waiting_list', 'category', 'year', 'borrow_count']
        books_df = books_df[column_order]

        # Initialize the DataManager with the DataFrame
        data_manager = DataManager.get_instance()
        data_manager.initialize_data(books_df)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_books_to_file(file_path="books.csv"):
    """Save the updated DataFrame from DataManager to a file."""
    try:
        # Get the DataFrame from DataManager
        data_manager = DataManager.get_instance()
        books_df = data_manager.get_data()

        # Save the DataFrame to the file
        books_df.to_csv(file_path, index=False)
        print(f"All updated data successfully saved to {file_path}.")
    except Exception as e:
        print(f"Error saving the updated DataFrame: {e}")

def row_to_book(row):
    """Convert a DataFrame row to a Book object."""
    try:
        book = Book(
            title=row['title'],
            author=row['author'],
            year=int(row['year']),
            category=row['category'],
            copies=int(row['copies'])
        )
        book.borrow_count = row['borrow_count']
        book.is_loaned = row['is_loaned']
        book.waiting_list = row['waiting_list']
        return book
    except KeyError as e:
        print(f"Missing key in the row: {e}")
    except Exception as e:
        print(f"Error converting row to Book: {e}")

def update_book_in_dataframe(book):
    """Update a row in the DataFrame managed by DataManager based on the Book object."""
    try:
        # Get the DataFrame from DataManager
        data_manager = DataManager.get_instance()
        books_df = data_manager.get_data()

        # Locate the row to update
        row_index = books_df[books_df['title'] == book.title].index[0]

        # Update the row with data from the Book object
        books_df.at[row_index, 'is_loaned'] = book.is_loaned
        books_df.at[row_index, 'available'] = sum(1 for status in book.is_loaned.values() if status == 'no')
        books_df.at[row_index, 'copies'] = book.copies
        books_df.at[row_index, 'waiting_list'] = book.waiting_list

    except IndexError:
        print(f"Error: Book '{book.title}' not found in the DataFrame.")
    except Exception as e:
        print(f"Error updating the DataFrame: {e}")

