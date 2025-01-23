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

def adjust_is_loaned(row):
    """
    Adjust the 'is_loaned' value to ensure it matches the number of copies.
    Expands or truncates the dictionary based on the number of copies.

    Args:
        row (pd.Series): A row from the DataFrame.

    Returns:
        dict: Updated 'is_loaned' dictionary.
    """
    num_copies = row['copies']
    is_loaned_dict = eval(row['is_loaned']) if isinstance(row['is_loaned'], str) else row['is_loaned']

    # Adjust the size of the dictionary
    is_loaned_dict = {
        i + 1: is_loaned_dict.get(i + 1, 'no') for i in range(num_copies)
    }

    return is_loaned_dict
def parse_is_loaned(value, num_copies):
    """
    Parses the 'is_loaned' value from the CSV into a valid dictionary.

    Args:
        value (str): The raw 'is_loaned' value from the CSV.
        num_copies (int): The number of copies of the book.

    Returns:
        dict: A dictionary representing the loan status of each copy.
    """
    if isinstance(value, str):
        value = value.strip()
        if value.lower() == 'no':  # All copies are available
            return {i + 1: 'no' for i in range(num_copies)}
        elif value.lower() == 'yes':  # All copies are loaned
            return {i + 1: 'yes' for i in range(num_copies)}
        else:
            try:
                # Try to evaluate the string as a dictionary
                return eval(value)
            except Exception as e:
                raise ValueError(f"Unexpected is_loaned value: {value}") from e
    elif isinstance(value, dict):
        return value
    else:
        raise ValueError(f"Unexpected is_loaned value type: {type(value)}")



def load_books_from_file(file_path="books.csv"):
    """
    Load books from a CSV file into a DataFrame and initialize the DataManager.
    """
    try:
        # Load the CSV into a DataFrame
        books_df = pd.read_csv(file_path)

        # Parse 'is_loaned' values and adjust based on 'copies'
        books_df['is_loaned'] = books_df.apply(
            lambda row: parse_is_loaned(row['is_loaned'], row['copies']),
            axis=1
        )

        # Add 'available' column based on 'is_loaned'
        books_df['available'] = books_df['is_loaned'].apply(
            lambda loaned_dict: sum(1 for status in loaned_dict.values() if status == 'no')
        )

        # Add 'waiting_list' column as empty lists if not exists
        if 'waiting_list' not in books_df.columns:
            books_df['waiting_list'] = [[] for _ in range(len(books_df))]


        # Calculate 'borrow_count' based on 'is_loaned'
        books_df['borrow_count'] = books_df['is_loaned'].apply(
            lambda loaned_dict: sum(1 for status in loaned_dict.values() if status == 'yes')
        )

        # Add 'popularity_score' column
        books_df['popularity_score'] = books_df['borrow_count'] + books_df['waiting_list'].apply(len)

        # Initialize the DataManager with the DataFrame
        data_manager = DataManager.get_instance()
        data_manager.initialize_data(books_df)

        print("Books loaded successfully.")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_books_to_file(file_path="books.csv"):
    """
    Save the updated DataFrame from DataManager to a file.
    """
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
    """
    Convert a DataFrame row to a Book object.
    """
    try:
        # Ensure all required keys exist
        required_keys = ['title', 'author', 'year', 'genre', 'copies', 'borrow_count', 'is_loaned', 'waiting_list']
        for key in required_keys:
            if key not in row:
                raise KeyError(f"Missing key: {key}")

        # Create the Book object
        book = Book(
            title=row['title'],
            author=row['author'],
            year=int(row['year']),
            category=row.get('genre', 'Unknown'),  # Map 'genre' to 'category'
            copies=int(row['copies'])
        )
        book.borrow_count = row.get('borrow_count', 0)
        book.is_loaned = row.get('is_loaned', {})
        book.waiting_list = row.get('waiting_list', [])
        return book

    except KeyError as e:
        print(f"Missing key in the row: {e}")
        return None
    except Exception as e:
        print(f"Error converting row to Book: {e}")
        return None


def update_book_in_dataframe(book):
    """
    Update a row in the DataFrame managed by DataManager based on the Book object.
    """
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
        books_df.at[row_index, 'borrow_count'] = book.borrow_count
        books_df.at[row_index, 'popularity_score'] = book.popularity_score

    except IndexError:
        print(f"Error: Book '{book.title}' not found in the DataFrame.")
    except Exception as e:
        print(f"Error updating the DataFrame: {e}")
