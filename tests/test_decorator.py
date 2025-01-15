import unittest
from models.book import Book
from models.book_decorator import BookDecorator

class TestBookDecorator(unittest.TestCase):
    def setUp(self):
        self.book = Book(1, "Clean Code", "Robert C. Martin", "Programming", 2008, 3)
        self.decorated_book = BookDecorator(self.book)

    def test_initial_borrow_count(self):
        self.assertEqual(self.decorated_book.get_borrow_count(), 0)

    def test_increase_popularity(self):
        self.decorated_book.increase_popularity()
        self.assertEqual(self.decorated_book.get_borrow_count(), 1)

    def test_multiple_increases(self):
        for _ in range(5):
            self.decorated_book.increase_popularity()
        self.assertEqual(self.decorated_book.get_borrow_count(), 5)

if __name__ == '__main__':
    unittest.main()
