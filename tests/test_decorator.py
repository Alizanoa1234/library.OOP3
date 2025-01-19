import unittest
import pandas as pd
from models.book_decorator import BookDecorator


class TestBookDecorator(unittest.TestCase):
    @staticmethod
    def create_books_data():
        """
        Creates a DataFrame with sample book data for testing.

        Returns:
            pd.DataFrame: A DataFrame containing sample books data.
        """
        return pd.DataFrame([
            {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "year": 2008, "copies": 3},
            {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "Programming", "year": 1999, "copies": 2},
            {"id": 3, "title": "Code Complete", "author": "Steve McConnell", "genre": "Programming", "year": 2004, "copies": 5}
        ])

    def setUp(self):
        """
        Set up the test environment with sample book data and initialize the BookDecorator.
        """
        self.books_data = self.create_books_data()
        self.decorator = BookDecorator(self.books_data)

    def test_initial_borrow_count(self):
        """
        Test that the initial borrow count for all books is 0.
        """
        for book_id in self.books_data["id"]:
            self.assertEqual(self.decorator.get_borrow_count(book_id), 0)

    def test_increase_borrow_count(self):
        """
        Test that increasing the borrow count updates the DataFrame correctly.
        """
        # Increment borrow count for a specific book
        self.decorator.books_df.loc[self.decorator.books_df["id"] == 1, "borrow_count"] += 1
        self.assertEqual(self.decorator.get_borrow_count(1), 1)

    def test_multiple_increases(self):
        """
        Test multiple borrow count increases.
        """
        self.decorator.books_df.loc[self.decorator.books_df["id"] == 1, "borrow_count"] += 5
        self.assertEqual(self.decorator.get_borrow_count(1), 5)

    def test_get_most_popular_books(self):
        """
        Test retrieving the most popular books.
        """
        # Set custom borrow counts
        self.decorator.books_df.loc[self.decorator.books_df["id"] == 1, "borrow_count"] += 5
        self.decorator.books_df.loc[self.decorator.books_df["id"] == 2, "borrow_count"] += 3
        self.decorator.books_df.loc[self.decorator.books_df["id"] == 3, "borrow_count"] += 8

        # Get top 2 most popular books
        most_popular = self.decorator.get_most_popular_books(top_n=2)
        self.assertEqual(len(most_popular), 2)
        self.assertEqual(most_popular.iloc[0]["id"], 3)  # Most popular book ID
        self.assertEqual(most_popular.iloc[1]["id"], 1)  # Second most popular book ID

    def test_get_borrow_count_invalid_id(self):
        """
        Test that an invalid book ID returns a borrow count of 0.
        """
        self.assertEqual(self.decorator.get_borrow_count(999), 0)  # ID 999 does not exist


if __name__ == '__main__':
    unittest.main()
