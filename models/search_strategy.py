import pandas as pd
from abc import ABC, abstractmethod

# Abstract base class for search strategy
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books_df, criteria):
        """
        Abstract method that all subclasses must implement.
        Args:
            books_df (pd.DataFrame): The DataFrame containing the books data.
            criteria (str): The search criteria.
        Returns:
            pd.DataFrame: Subset of the books DataFrame matching the criteria.
        """
        pass


class SearchByName(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["title"].str.contains(criteria, case=False, na=False)]


class SearchByAuthor(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["author"].str.contains(criteria, case=False, na=False)]


class SearchByCategory(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["category"].str.contains(criteria, case=False, na=False)]


class SearchByYear(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["year"].astype(str).str.contains(criteria, case=False, na=False)]


class SearchByID(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["id"] == int(criteria)]


# Manager class for handling different search strategies
class SearchManager:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, books_df, criteria):
        return self.strategy.search(books_df, criteria)
