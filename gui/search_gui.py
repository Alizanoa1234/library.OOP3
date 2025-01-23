import tkinter as tk
from data.books import load_books_from_file
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor
from logs.actions import log_info, log_error

BOOKS_FILE = "books.csv"


def open_search_gui(log_text, search_type):
    try:
        books_df = load_books_from_file(BOOKS_FILE)
    except Exception as e:
        log_error(f"Error loading books file: {e}")
        log_text.insert("end", "Error: Could not load books file.\n")
        return

    window = tk.Toplevel()
    window.title(f"{search_type.capitalize()} Books")

    tk.Label(window, text="Enter Search Query (if applicable):").pack()
    query_entry = tk.Entry(window)
    query_entry.pack()

    result_text = tk.Text(window, wrap="word", height=15, width=50, state="normal")
    result_text.pack(pady=10)

    def handle_search():
        query = query_entry.get().strip()
        if not query and search_type in ["search", "popular"]:
            result_text.insert("end", "Error: Query is required for this search.\n", "error")
            return

        try:
            search_manager = SearchManager(SearchByName()) if search_type == "search" else None
            if search_type == "search":
                search_manager.set_strategy(SearchByName())
                results = search_manager.search(books_df, query)
                log_info(f"Search by name completed for '{query}'.")

            elif search_type == "author":
                search_manager.set_strategy(SearchByAuthor())
                results = search_manager.search(books_df, query)
                log_info(f"Search by author completed for '{query}'.")

            elif search_type == "view":
                results = books_df
                log_info("Displayed all books successfully.")

            elif search_type == "popular":
                results = books_df.sort_values(by="popularity_score", ascending=False).head(10)
                log_info("Displayed popular books successfully.")

            if not results.empty:
                result_text.delete("1.0", "end")
                result_text.insert("end", results.to_string(index=False) + "\n")
                log_text.insert("end", f"{search_type.capitalize()} successful.\n")
            else:
                result_text.delete("1.0", "end")
                result_text.insert("end", "No results found.\n")
                log_text.insert("end", f"No results found for {search_type}.\n")
        except Exception as e:
            log_error(f"Error in {search_type}: {e}")
            log_text.insert("end", f"Error during {search_type}: {e}\n")

    tk.Button(window, text="Search", command=handle_search).pack(pady=10)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)
