import unittest
from models.book import Book
from services.library_manager import LibraryManager

class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        self.library_manager = LibraryManager()
        self.book = Book(1, "Clean Code", "Robert C. Martin", "Programming", 2008, 2)
        self.library_manager.add_book(self.book)

    def test_borrow_book_success(self):
        result = self.library_manager.borrow_book(1)
        self.assertTrue(result)
        self.assertEqual(self.book.available, 1)

    def test_borrow_book_no_copies(self):
        self.library_manager.borrow_book(1)
        self.library_manager.borrow_book(1)
        result = self.library_manager.borrow_book(1)
        self.assertFalse(result)

    def test_return_book(self):
        self.library_manager.borrow_book(1)
        self.library_manager.return_book(1)
        self.assertEqual(self.book.available, 2)

if __name__ == '__main__':
    unittest.main()
