import pandas as pd

class BookDecorator:
    """
    A decorator for a DataFrame of books that tracks the popularity of books
    based on the number of times they have been borrowed.
    """

    def __init__(self, books_df: pd.DataFrame):
        """
        Initializes the BookDecorator with a DataFrame of books.

        Args:
            books_df (pd.DataFrame): The DataFrame containing the books data.
        """
        self.books_df = books_df.copy()
        if "borrow_count" not in self.books_df.columns:
            self.books_df["borrow_count"] = 0  # Add a column to track borrow counts

    def get_borrow_count(self, book_id: int) -> int:
        """
        Gets the borrow count for a specific book by its ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            int: The borrow count for the specified book.
        """
        if book_id in self.books_df["id"].values:
            return int(self.books_df.loc[self.books_df["id"] == book_id, "borrow_count"].values[0])
        else:
            print(f"Book ID {book_id} not found.")
            return 0

    def get_most_popular_books(self, top_n: int = 5) -> pd.DataFrame:
        """
        Returns the top N most popular books based on borrow count.

        Args:
            top_n (int): The number of top books to return.

        Returns:
            pd.DataFrame: A DataFrame containing the top N most popular books.
        """
        return self.books_df.sort_values(by="borrow_count", ascending=False).head(top_n)

    def __str__(self):
        """
        Returns a string representation of the decorated DataFrame.

        Returns:
            str: A string with the books and their borrow counts.
        """
        return str(self.books_df)
