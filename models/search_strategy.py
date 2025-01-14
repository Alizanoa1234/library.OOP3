from abc import ABC, abstractmethod

# Abstract base class for search strategy
class SearchStrategy(ABC):
    # Abstract method that all subclasses must implement
    @abstractmethod
    def search(self, books, criteria):
        pass

# Search by book title
class SearchByName(SearchStrategy):
    # Implements search logic for matching the title
    def search(self, books, criteria):
        return [book for book in books if criteria.lower() in book.title.lower()]

# Search by book author
class SearchByAuthor(SearchStrategy):
    # Implements search logic for matching the author
    def search(self, books, criteria):
        return [book for book in books if criteria.lower() in book.author.lower()]

# Search by book category
class SearchByCategory(SearchStrategy):
    # Implements search logic for matching the category
    def search(self, books, criteria):
        return [book for book in books if criteria.lower() in book.category.lower()]

class SearchByYear(SearchStrategy):
    def search(self, books, criteria):
        return [book for book in books if book.year == int(criteria)]

class SearchByID(SearchStrategy):
    def search(self, books, criteria):
        return [book for book in books if book.id == int(criteria)]




# Manager class for handling different search strategies
class SearchManager:
    # Initializes the manager with a specific search strategy
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    # Allows changing the search strategy at runtime
    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    # Executes the current strategy's search function
    def search(self, books, criteria):
        return self.strategy.search(books, criteria)


#איך קורים לSERCHSRATGY
## טעינת ספרים מקובץ CSV
# books = load_books_from_file('books.csv')
#
# # חיפוש לפי שם ספר
# search_manager = SearchManager(SearchByName())
# results_by_name = search_manager.search(books, "Python")
# print(f"Books found by name: {[book.title for book in results_by_name]}")
#
# # מעבר לחיפוש לפי מחבר
# search_manager.set_strategy(SearchByAuthor())
# results_by_author = search_manager.search(books, "Mark Twain")
# print(f"Books found by author: {[book.title for book in results_by_author]}")
