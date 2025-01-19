import unittest
import pandas as pd
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear

class TestSearchStrategies(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample DataFrame of books and initialize the SearchManager.
        """
        self.books_df = pd.DataFrame([
            {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "category": "Programming", "year": 2008},
            {"id": 2, "title": "The Pragmatic Programmer", "author": "Andy Hunt", "category": "Programming", "year": 1999},
            {"id": 3, "title": "Design Patterns", "author": "Erich Gamma", "category": "Software Design", "year": 1994},
        ])
        self.search_manager = SearchManager(SearchByName())  # Default strategy: SearchByName

    def test_search_by_name(self):
        """
        Test searching by book title.
        """
        results = self.search_manager.search(self.books_df, "Clean Code")
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]["title"], "Clean Code")

    def test_search_by_author(self):
        """
        Test searching by author.
        """
        self.search_manager.set_strategy(SearchByAuthor())
        results = self.search_manager.search(self.books_df, "Robert C. Martin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]["author"], "Robert C. Martin")

    def test_search_by_category(self):
        """
        Test searching by category.
        """
        self.search_manager.set_strategy(SearchByCategory())
        results = self.search_manager.search(self.books_df, "Programming")
        self.assertEqual(len(results), 2)

    def test_search_by_year(self):
        """
        Test searching by year.
        """
        self.search_manager.set_strategy(SearchByYear())
        results = self.search_manager.search(self.books_df, "1994")
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]["year"], 1994)

    def test_search_no_results(self):
        """
        Test searching for a non-existent book.
        """
        results = self.search_manager.search(self.books_df, "Non-Existent Book")
        self.assertTrue(results.empty)

if __name__ == '__main__':
    unittest.main()
