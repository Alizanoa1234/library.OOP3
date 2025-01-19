import unittest
import os
import pandas as pd
from models.book import Book
from services.library_manager import LibraryManager

class TestLibraryManager(unittest.TestCase):
    TEST_FILE = "test_books.csv"

    def setUp(self):
        """
        Set up a temporary CSV file for testing and initialize the LibraryManager.
        """
        self.books_data = pd.DataFrame([
            {"title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "year": 2008, "copies": 2, "available": 2, "borrow_count": 0},
            {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "Programming", "year": 1999, "copies": 1, "available": 1, "borrow_count": 0}
        ])
        self.books_data.to_csv(self.TEST_FILE, index=False)
        self.library_manager = LibraryManager(self.TEST_FILE)

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_add_book(self):
        new_book = Book("Code Complete", "Steve McConnell", "Programming", 2004, 3)
        result = self.library_manager.add_book(new_book)
        self.assertTrue(result)
        df = pd.read_csv(self.TEST_FILE)
        self.assertIn("Code Complete", df["title"].values)

    def test_borrow_book(self):
        result = self.library_manager.borrow_book("Clean Code", "Robert C. Martin")
        self.assertTrue(result)
        book = next(b for b in self.library_manager.books if b.title == "Clean Code")
        self.assertEqual(book.available, 1)

    def test_return_book(self):
        self.library_manager.borrow_book("Clean Code", "Robert C. Martin")
        result = self.library_manager.return_book("Clean Code", "Robert C. Martin")
        self.assertTrue(result)
        book = next(b for b in self.library_manager.books if b.title == "Clean Code")
        self.assertEqual(book.available, 2)

    def test_remove_book(self):
        result = self.library_manager.remove_book("Clean Code", "Robert C. Martin")
        self.assertTrue(result)
        df = pd.read_csv(self.TEST_FILE)
        self.assertNotIn("Clean Code", df["title"].values)

if __name__ == "__main__":
    unittest.main()
