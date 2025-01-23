import tkinter as tk
from logs.actions import log_info
from data.books import load_books_from_file
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor

BOOKS_FILE = "books.csv"
books_df = load_books_from_file(BOOKS_FILE)

def open_search_gui():
    """Search Books GUI."""
    search_manager = SearchManager(SearchByName())

    def search_by_name():
        query = search_entry.get().strip()
        results = search_manager.search(books_df, query)
        display_results(results, f"Search by name '{query}'")

    def search_by_author():
        query = search_entry.get().strip()
        search_manager.set_strategy(SearchByAuthor())
        results = search_manager.search(books_df, query)
        display_results(results, f"Search by author '{query}'")

    def display_results(results, log_message):
        result_text.delete(1.0, tk.END)
        if results.empty:
            result_text.insert(tk.END, "No results found.\n")
            log_info(f"{log_message} failed.")
        else:
            for _, book in results.iterrows():
                result_text.insert(tk.END, f"{book['title']} by {book['author']}\n")
            log_info(f"{log_message} succeeded.")

    # GUI window
    window = tk.Toplevel()
    window.title("Search Books")

    tk.Label(window, text="Search Query").pack()
    search_entry = tk.Entry(window)
    search_entry.pack()

    tk.Button(window, text="Search by Name", command=search_by_name).pack(pady=5)
    tk.Button(window, text="Search by Author", command=search_by_author).pack(pady=5)

    result_text = tk.Text(window, height=20, width=50)
    result_text.pack()

    window.mainloop()
