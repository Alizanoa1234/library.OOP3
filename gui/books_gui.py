import tkinter as tk
import pandas as pd
from logs.actions import log_info, log_error
from data.books import load_books_from_file, save_books_to_file

BOOKS_FILE = "books.csv"

def open_books_gui(action):
    """Handles the Books Management GUI."""
    books_df = load_books_from_file(BOOKS_FILE)

    def add_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        if not title or not author:
            result_label.config(text="Title and Author are required!", fg="red")
            return

        if not books_df[(books_df['title'] == title) & (books_df['author'] == author)].empty:
            result_label.config(text="Book already exists!", fg="red")
            log_error(f"Failed to add book '{title}' by '{author}': Already exists.")
            return

        new_book = pd.DataFrame([{
            "title": title,
            "author": author,
            "is_loaned": "No",
            "copies": 1,
            "genre": "Unknown",
            "year": "Unknown"
        }])
        save_books_to_file(pd.concat([books_df, new_book], ignore_index=True))
        result_label.config(text="Book added successfully!", fg="green")
        log_info(f"Book '{title}' by '{author}' added successfully.")

    def remove_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        mask = (books_df["title"] == title) & (books_df["author"] == author)
        if books_df[mask].empty:
            result_label.config(text="Book not found!", fg="red")
            log_error(f"Failed to remove book '{title}' by '{author}': Not found.")
            return

        books_df.drop(books_df[mask].index, inplace=True)
        save_books_to_file(books_df)
        result_label.config(text="Book removed successfully!", fg="green")
        log_info(f"Book '{title}' by '{author}' removed successfully.")

    def view_books():
        result_text.delete(1.0, tk.END)
        try:
            for _, book in books_df.iterrows():
                result_text.insert(tk.END, f"{book['title']} by {book['author']} (Genre: {book['genre']})\n")
            log_info("Displayed all books successfully.")
        except Exception as e:
            result_label.config(text=f"Error displaying books: {e}", fg="red")

    def popular_books():
        result_text.delete(1.0, tk.END)
        try:
            popular_books_df = books_df.sort_values("copies", ascending=False).head(10)
            for _, book in popular_books_df.iterrows():
                result_text.insert(tk.END, f"{book['title']} by {book['author']} (Copies: {book['copies']})\n")
            log_info("Displayed popular books successfully.")
        except Exception as e:
            result_label.config(text=f"Error displaying popular books: {e}", fg="red")

    # GUI window
    window = tk.Toplevel()
    window.title("Books Management")

    tk.Label(window, text=f"Action: {action.capitalize()}", font=("Arial", 16, "bold")).pack(pady=10)

    if action in ["add", "remove"]:
        tk.Label(window, text="Title").pack()
        title_entry = tk.Entry(window)
        title_entry.pack()

        tk.Label(window, text="Author").pack()
        author_entry = tk.Entry(window)
        author_entry.pack()

        if action == "add":
            tk.Button(window, text="Add Book", command=add_book).pack(pady=5)
        elif action == "remove":
            tk.Button(window, text="Remove Book", command=remove_book).pack(pady=5)

    elif action == "view":
        tk.Button(window, text="View All Books", command=view_books).pack(pady=5)

    elif action == "popular":
        tk.Button(window, text="View Popular Books", command=popular_books).pack(pady=5)

    result_label = tk.Label(window, text="", font=("Arial", 12))
    result_label.pack()

    result_text = tk.Text(window, height=20, width=50)
    result_text.pack()

    window.mainloop()
