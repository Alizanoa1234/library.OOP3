import unittest
from models.book import Book
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory

class TestSearchStrategies(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book(1, "Clean Code", "Robert C. Martin", "Programming", 2008, 3),
            Book(2, "The Pragmatic Programmer", "Andy Hunt", "Programming", 1999, 1)
        ]
        self.search_manager = SearchManager(SearchByName())

    def test_search_by_name(self):
        results = self.search_manager.search(self.books, "Clean Code")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Clean Code")

    def test_search_by_author(self):
        self.search_manager.set_strategy(SearchByAuthor())
        results = self.search_manager.search(self.books, "Robert C. Martin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Robert C. Martin")

    def test_search_by_category(self):
        self.search_manager.set_strategy(SearchByCategory())
        results = self.search_manager.search(self.books, "Programming")
        self.assertEqual(len(results), 2)

if __name__ == '__main__':
    unittest.main()
