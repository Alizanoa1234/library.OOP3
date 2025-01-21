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
    def get_borrow_count(self, title_book: str) -> int:
        """
        Gets the borrow count for a specific book by its ID.

        Args:
            title_book (str): The name of the book.

        Returns:
            int: The borrow count for the specified book.
        """
        if title_book in self.books_df["title"].values:
            return int(self.books_df.loc[self.books_df["title"] == title_book, "borrow_count"].values[0])
        else:
            print(f"Book name {title_book} not found.")
            return 0

    def get_most_popular_books(self, top_n: int = 10) -> pd.DataFrame:
        """
        Returns the top N most popular books based on the popularity score.
        Popularity score is calculated as the sum of borrow count and the size of the waiting list.

        Args:
            top_n (int): The number of top books to return.

        Returns:
            pd.DataFrame: A DataFrame containing the top N most popular books.
        """
        # Sort by popularity_score in descending order
        sorted_books = self.books_df.sort_values(by="popularity_score", ascending=False)

        # Return the top N books
        return sorted_books.head(top_n)

    def __str__(self):
        """
        Returns a string representation of the decorated DataFrame.

        Returns:
            str: A string with the books and their borrow counts.
        """
        return str(self.books_df)
