import tkinter as tk
from data.books import load_books_from_file
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor
from logs.actions import log_info, log_error
import pandas as pd


BOOKS_FILE = "books.csv"

def open_search_gui(log_text, search_type):
    try:
        # Load the books file
        books_df = load_books_from_file(BOOKS_FILE)
    except Exception as e:
        log_error(f"Error loading books file: {e}")
        log_text.insert("end", "Error: Could not load books file.\n")
        return

    # Create a new window for the search GUI
    window = tk.Toplevel()
    window.title(f"{search_type.capitalize()} Books")

    tk.Label(window, text="Enter Search Query (if applicable):").pack()
    query_entry = tk.Entry(window)
    query_entry.pack()

    result_text = tk.Text(window, wrap="word", height=15, width=50, state="normal")
    result_text.pack(pady=10)

    def handle_search():
        query = query_entry.get().strip()
        try:
            # Initialize search manager based on search type
            if search_type == "search":
                search_manager = SearchManager(SearchByName())
                results = search_manager.search(books_df, query)
                log_info(f"Search by name completed for '{query}'.")
            elif search_type == "author":
                search_manager = SearchManager(SearchByAuthor())
                results = search_manager.search(books_df, query)
                log_info(f"Search by author completed for '{query}'.")
            elif search_type == "view":
                results = books_df
                log_info("Displayed all books successfully.")
            elif search_type == "popular":
                results = books_df.sort_values(by="popularity_score", ascending=False).head(10)
                log_info("Displayed popular books successfully.")
            else:
                results = pd.DataFrame()

            # Display results in the GUI
            result_text.delete("1.0", "end")
            if not results.empty:
                result_text.insert("end", results.to_string(index=False) + "\n")
                log_text.insert("end", f"{search_type.capitalize()} successful.\n")
            else:
                result_text.insert("end", "No results found.\n")
                log_text.insert("end", f"No results found for {search_type}.\n")

        except Exception as e:
            log_error(f"Error in {search_type}: {e}")
            log_text.insert("end", f"Error during {search_type}: {e}\n")

    # Add buttons for searching and closing
    tk.Button(window, text="Search", command=handle_search).pack(pady=10)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)
