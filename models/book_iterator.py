import pandas as pd

from models.book import Book


class BookIterator:
    """
    An iterator for navigating through a DataFrame of books.
    """

    def __init__(self, books_df: pd.DataFrame):
        """
        Initializes the iterator with a DataFrame of books.

        Args:
            books_df (pd.DataFrame): The DataFrame containing the books data.
        """
        if books_df.empty:
            raise ValueError("The books DataFrame is empty. Cannot initialize iterator.")

        self.books_df = books_df.reset_index(drop=True)  # Ensure consistent indexing
        self.index = 0

    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self

    def __next__(self):
        """
        Returns the next book (as a Book object) in the DataFrame.
        """
        if self.index >= len(self.books_df):
            raise StopIteration
        row = self.books_df.iloc[self.index]
        self.index += 1
        return Book(
            title=row['title'],
            author=row['author'],
            year=row['year'],
            category=row['category'],
            copies=row['copies']
        )

    def reset(self):
        """
        Resets the iterator to the beginning of the DataFrame.
        """
        self.index = 0

    def filter(self, **kwargs):
        """
        Filters the DataFrame based on given criteria and resets the iterator.

        Args:
            kwargs: Column-value pairs to filter the DataFrame.
                   Supports conditions like column__lt=value or column__contains=value.
        """
        filtered_df = self.books_df
        for column, value in kwargs.items():
            if "__" in column:
                col, op = column.split("__")
                if op == "lt":  # Less than
                    filtered_df = filtered_df[filtered_df[col] < value]
                elif op == "gt":  # Greater than
                    filtered_df = filtered_df[filtered_df[col] > value]
                elif op == "contains":  # String contains
                    filtered_df = filtered_df[filtered_df[col].str.contains(value, na=False)]
            else:
                filtered_df = filtered_df[filtered_df[column] == value]
        self.books_df = filtered_df.reset_index(drop=True)
        self.reset()

    def paginate(self, page_size: int):
        """
        Returns a generator that yields pages of books.

        Args:
            page_size (int): The number of rows per page. Must be greater than 0.

        Yields:
            pd.DataFrame: A subset of the books DataFrame for each page.

        Raises:
            ValueError: If page_size is less than or equal to 0.
        """
        if page_size <= 0:
            raise ValueError("Page size must be greater than 0.")
        for start in range(0, len(self.books_df), page_size):
            yield self.books_df.iloc[start:start + page_size]
def to_dict_list(self):
    """
    Converts the DataFrame to a list of dictionaries.
    Useful for GUI table rendering.

    Returns:
        list: A list of dictionaries representing the books.
    """
    return self.books_df.to_dict(orient="records")
def get_page(self, page: int, page_size: int):
    """
    Returns a specific page of books as a DataFrame or list of dictionaries.

    Args:
        page (int): The page number (starting from 1).
        page_size (int): The number of books per page.

    Returns:
        pd.DataFrame: A subset of the books DataFrame for the requested page.
    """
    start = (page - 1) * page_size
    end = start + page_size
    if start >= len(self.books_df):
        raise ValueError("Page number exceeds total pages.")
    return self.books_df.iloc[start:end]
def get_total_pages(self, page_size: int):
    """
    Calculate the total number of pages based on the page size.

    Args:
        page_size (int): The number of rows per page.

    Returns:
        int: Total number of pages.
    """
    import math
    return math.ceil(len(self.books_df) / page_size)
