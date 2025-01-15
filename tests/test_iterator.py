import unittest
from models.book import Book
from models.book_iterator import BookIterator

class TestBookIterator(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book(1, "Clean Code", "Robert C. Martin", "Programming", 2008, 3),
            Book(2, "The Pragmatic Programmer", "Andy Hunt", "Programming", 1999, 1)
        ]
        self.iterator = BookIterator(self.books)

    def test_iteration(self):
        book_titles = [book.title for book in self.iterator]
        self.assertEqual(book_titles, ["Clean Code", "The Pragmatic Programmer"])

    def test_empty_iterator(self):
        empty_iterator = BookIterator([])
        with self.assertRaises(StopIteration):
            next(iter(empty_iterator))

if __name__ == '__main__':
    unittest.main()
