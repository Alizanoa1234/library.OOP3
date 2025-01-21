import tkinter as tk
from tkinter import ttk, messagebox
from services.library_manager import LibraryManager
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByCategory, SearchByYear
import pandas as pd


class SearchGUI:
    """
    GUI for searching books using different strategies.
    """

    def __init__(self, root, library_manager):
        """
        Initializes the SearchGUI.

        Args:
            root (Tk): The main Tkinter window or Toplevel.
            library_manager (LibraryManager): The LibraryManager instance for managing book data.
        """
        self.root = tk.Toplevel(root)
        self.root.title("Search Books")
        self.root.geometry("600x400")
        self.library_manager = library_manager

        # Initialize SearchManager with a default strategy
        self.search_manager = SearchManager(SearchByName())

        # Create the GUI components
        self.create_search_menu()

    def create_search_menu(self):
        """
        Creates the main search menu with options for selecting search criteria and displaying results.
        """
        tk.Label(self.root, text="Search Books", font=("Helvetica", 16)).pack(pady=10)

        # Search input field
        tk.Label(self.root, text="Search Term:").pack()
        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.pack(pady=5)

        # Dropdown menu for selecting search strategy
        tk.Label(self.root, text="Search By:").pack()
        self.strategy_var = tk.StringVar(value="Name")
        self.strategy_menu = ttk.Combobox(
            self.root,
            textvariable=self.strategy_var,
            values=["Name", "Author", "Category", "Year"],
            state="readonly",
        )
        self.strategy_menu.pack(pady=5)

        # Search button
        tk.Button(self.root, text="Search", command=self.perform_search).pack(pady=10)

        # Table for displaying search results
        self.tree = ttk.Treeview(
            self.root,
            columns=("Title", "Author", "Year", "Category"),
            show="headings",
        )
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Category", text="Category")
        self.tree.pack(fill="both", expand=True, pady=10)

        # Back button
        tk.Button(self.root, text="Back", command=self.root.destroy).pack(pady=10)

    def perform_search(self):
        """
        Performs the search based on the selected strategy and input criteria.
        """
        search_term = self.search_entry.get().strip()
        search_by = self.strategy_var.get()

        # Validate input
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term.")
            return

        # Map the selected strategy to the corresponding class
        strategy_mapping = {
            "Name": SearchByName(),
            "Author": SearchByAuthor(),
            "Category": SearchByCategory(),
            "Year": SearchByYear(),
        }

        # Set the appropriate search strategy
        self.search_manager.set_strategy(strategy_mapping.get(search_by, SearchByName()))

        # Get the books as a DataFrame
        try:
            books_df = self.library_manager.get_all_books()

            # Perform the search
            results = self.search_manager.search(books_df, search_term)

            # Display the results
            self.populate_table(results)
            if not results.empty:
                messagebox.showinfo("Success", f"Search by {search_by} completed successfully.")
            else:
                messagebox.showinfo("No Results", "No books found matching your criteria.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the search: {e}")

    def populate_table(self, results):
        """
        Populates the TreeView table with search results.

        Args:
            results (pd.DataFrame): The search results as a DataFrame.
        """
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add new rows
        for _, book in results.iterrows():
            self.tree.insert("", "end", values=(book["title"], book["author"], book["year"], book["category"]))
