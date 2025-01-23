import unittest
import pandas as pd
from data.books import (
    DataManager,
    adjust_is_loaned,
    parse_is_loaned,
    load_books_from_file,
    save_books_to_file,
    row_to_book,
    update_book_in_dataframe,
)
from models.book import Book


class TestBooksFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup data and environment for all tests."""
        cls.sample_data = pd.DataFrame([
            {"title": "Book1", "author": "Author1", "copies": 3, "is_loaned": "{1: 'no', 2: 'no', 3: 'no'}", "genre": "Fiction", "year": 2001},
            {"title": "Book2", "author": "Author2", "copies": 2, "is_loaned": "{1: 'yes', 2: 'no'}", "genre": "Drama", "year": 2010},
            {"title": "Book3", "author": "Author3", "copies": 1, "is_loaned": "no", "genre": "Thriller", "year": 2005},
        ])
        cls.file_path = "test_books.csv"
        cls.sample_data.to_csv(cls.file_path, index=False)
        cls.data_manager = DataManager.get_instance()
        cls.data_manager.initialize_data(cls.sample_data)

    def test_adjust_is_loaned(self):
        """Test if the adjust_is_loaned function properly adjusts the dictionary."""
        row = {"copies": 4, "is_loaned": {1: "no", 2: "yes"}}
        result = adjust_is_loaned(row)
        expected = {1: "no", 2: "yes", 3: "no", 4: "no"}
        self.assertEqual(result, expected)

    def test_parse_is_loaned(self):
        """Test if the parse_is_loaned function parses various formats correctly."""
        result = parse_is_loaned("no", 3)
        expected = {1: "no", 2: "no", 3: "no"}
        self.assertEqual(result, expected)

        result = parse_is_loaned("{1: 'yes', 2: 'no'}", 3)
        expected = {1: "yes", 2: "no", 3: "no"}
        self.assertEqual(result, expected)

        with self.assertRaises(ValueError):
            parse_is_loaned("invalid_string", 2)

    def test_load_books_from_file(self):
        """Test loading books from a file into the DataFrame."""
        load_books_from_file(self.file_path)
        data = self.data_manager.get_data()
        self.assertEqual(len(data), 3)  # Check if 3 rows were loaded
        self.assertIn("available", data.columns)
        self.assertIn("borrow_count", data.columns)

    def test_save_books_to_file(self):
        """Test saving the updated DataFrame back to the file."""
        new_file_path = "test_books_saved.csv"
        save_books_to_file(new_file_path)
        saved_data = pd.read_csv(new_file_path)
        self.assertEqual(len(saved_data), 3)
        self.assertIn("available", saved_data.columns)

    def test_row_to_book(self):
        """Test converting a DataFrame row into a Book object."""
        row = {
            "title": "Book4",
            "author": "Author4",
            "year": 2015,
            "genre": "Horror",
            "copies": 5,
            "borrow_count": 2,
            "is_loaned": {1: "no", 2: "yes", 3: "no"},
            "waiting_list": [],
        }
        book = row_to_book(row)
        self.assertEqual(book.title, "Book4")
        self.assertEqual(book.copies, 5)
        self.assertEqual(book.is_loaned[1], "no")

    def test_update_book_in_dataframe(self):
        """Test updating a book's data in the DataFrame."""
        book = Book(
            title="Book1",
            author="Author1",
            year=2001,
            category="Fiction",
            copies=3,
        )
        book.is_loaned = {1: "yes", 2: "no", 3: "no"}
        book.borrow_count = 5
        book.waiting_list = ["User1"]

        update_book_in_dataframe(book)
        data = self.data_manager.get_data()
        updated_row = data[data["title"] == "Book1"].iloc[0]
        self.assertEqual(updated_row["borrow_count"], 5)
        self.assertEqual(updated_row["is_loaned"], {1: "yes", 2: "no", 3: "no"})

    def test_edge_cases(self):
        """Test edge cases for the functions."""
        # Test adjust_is_loaned with empty is_loaned and copies=0
        row = {"copies": 0, "is_loaned": {}}
        result = adjust_is_loaned(row)
        self.assertEqual(result, {})

        # Test parse_is_loaned with invalid string
        with self.assertRaises(ValueError):
            parse_is_loaned("invalid_string", 2)

        # Test loading an empty file
        empty_file_path = "empty_books.csv"
        pd.DataFrame().to_csv(empty_file_path, index=False)
        load_books_from_file(empty_file_path)
        data = self.data_manager.get_data()
        self.assertTrue(data.empty)

        # Test updating a book not in the DataFrame
        non_existent_book = Book(title="NonExistent", author="Author", year=2000, category="Unknown", copies=1)
        with self.assertLogs() as cm:
            update_book_in_dataframe(non_existent_book)
        self.assertIn("Error: Book 'NonExistent' not found", cm.output[0])


if __name__ == "__main__":
    unittest.main()
