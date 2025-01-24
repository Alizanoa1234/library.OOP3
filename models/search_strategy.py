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


class SearchByGenre(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["genre"].str.contains(criteria, case=False, na=False)]


class SearchByYear(SearchStrategy):
    def search(self, books_df, criteria):
        return books_df[books_df["year"].astype(str).str.contains(criteria, case=False, na=False)]


class SearchByID(SearchStrategy):
    def search(self, books_df, criteria):
        try:
            return books_df[books_df["title"].str.contains(criteria, case=False, na=False)]
        except Exception as e:
            print(f"Error during search: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error


class SearchByYearRange(SearchStrategy):
    def search(self, books_df, criteria):
        """
        Search books by a range of years.

        Args:
            books_df (pd.DataFrame): The DataFrame containing the books data.
            criteria (dict): Must include 'start_year' and 'end_year'.

        Returns:
            pd.DataFrame: Subset of the books DataFrame matching the year range.
        """
        try:
            start_year = int(criteria.get("start_year", 0))  # Default to 0 if not provided
            end_year = int(criteria.get("end_year", float("inf")))  # Default to infinity if not provided
            return books_df[(books_df["year"] >= start_year) & (books_df["year"] <= end_year)]
        except KeyError as e:
            print(f"Missing key in criteria: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in year range search: {e}")
            return pd.DataFrame()



# Manager class for handling different search strategies
class SearchManager:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, books_df, criteria):
        return self.strategy.search(books_df, criteria)

    def search_multiple(self, books_df, **kwargs):
        """
        Allows searching with multiple criteria.

        Args:
            books_df (pd.DataFrame): The books DataFrame.
            kwargs: Column-value pairs for filtering.

        Returns:
            pd.DataFrame: Filtered DataFrame based on criteria.
        """
        filtered_df = books_df
        for column, value in kwargs.items():
            filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, case=False, na=False)]
        return filtered_df
