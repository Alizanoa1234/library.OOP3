import unittest
import pandas as pd
from models.book_iterator import BookIterator


class TestBookIterator(unittest.TestCase):
    @staticmethod
    def create_books_data():
        """
        Create a DataFrame with sample book data for testing.

        Returns:
            pd.DataFrame: A DataFrame containing sample books data.
        """
        return pd.DataFrame([
            {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "year": 2008, "copies": 3},
            {"id": 2, "title": "The Pragmatic Programmer", "author": "Andy Hunt", "genre": "Programming", "year": 1999, "copies": 2},
            {"id": 3, "title": "Code Complete", "author": "Steve McConnell", "genre": "Programming", "year": 2004, "copies": 5},
            {"id": 4, "title": "Design Patterns", "author": "Erich Gamma", "genre": "Programming", "year": 1994, "copies": 1},
        ])

    def setUp(self):
        """
        Set up the test environment with sample book data and initialize the BookIterator.
        """
        self.books_data = self.create_books_data()
        self.iterator = BookIterator(self.books_data)

    def test_iteration(self):
        """
        Test that the iterator goes through all rows of the DataFrame.
        """
        titles = [row["title"] for row in self.iterator]
        expected_titles = self.books_data["title"].tolist()
        self.assertEqual(titles, expected_titles)

    def test_empty_iterator(self):
        """
        Test that initializing with an empty DataFrame raises a ValueError.
        """
        empty_df = pd.DataFrame(columns=self.books_data.columns)
        with self.assertRaises(ValueError):
            BookIterator(empty_df)

    def test_reset(self):
        """
        Test that resetting the iterator starts iteration from the beginning.
        """
        next(self.iterator)  # Advance the iterator by one
        self.iterator.reset()
        first_row = next(self.iterator)
        self.assertEqual(first_row["title"], "Clean Code")

    def test_filter(self):
        """
        Test that the filter method correctly filters the DataFrame.
        """
        self.iterator.filter(genre="Programming", year=2008)
        filtered_titles = [row["title"] for row in self.iterator]
        self.assertEqual(filtered_titles, ["Clean Code"])

    def test_paginate(self):
        """
        Test that the paginate method returns pages of the specified size.
        """
        pages = list(self.iterator.paginate(page_size=2))
        self.assertEqual(len(pages), 2)  # Two pages expected for 4 books
        self.assertEqual(pages[0]["title"].tolist(), ["Clean Code", "The Pragmatic Programmer"])
        self.assertEqual(pages[1]["title"].tolist(), ["Code Complete", "Design Patterns"])


if __name__ == "__main__":
    unittest.main()
