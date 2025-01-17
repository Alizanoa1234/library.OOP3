class BookIterator:
    """
    An iterator for navigating through a DataFrame of books.
    """

    def __init__(self, books_df: pd.DataFrame):
        """
        Initializes the iterator with a DataFrame of books.

        Args:
            books_df (pd.DataFrame): The DataFrame of books to iterate over.
        """
        self.books_df = books_df.reset_index(drop=True)  # Ensure proper indexing
        self.index = 0

    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self

    def __next__(self):
        """
        Returns the next book (row) in the DataFrame.

        Raises:
            StopIteration: When there are no more rows to iterate over.
        """
        if self.index >= len(self.books_df):
            raise StopIteration
        book = self.books_df.iloc[self.index]
        self.index += 1
        return book

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

        Example:
            iterator.filter(category="Fiction", year=2020)
        """
        filtered_df = self.books_df
        for key, value in kwargs.items():
            filtered_df = filtered_df[filtered_df[key] == value]
        self.books_df = filtered_df.reset_index(drop=True)
        self.reset()
