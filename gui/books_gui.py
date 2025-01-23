import tkinter as tk
import pandas as pd
from data.books import load_books_from_file, save_books_to_file
from logs.actions import log_info, log_error

BOOKS_FILE = "books.csv"

def open_books_gui(log_text, action):
    # Load books from the CSV file
    try:
        books_df = load_books_from_file(BOOKS_FILE)
    except Exception as e:
        log_error(f"Error loading books file: {e}")
        log_text.insert("end", f"Error: Could not load books file.\n")
        return

    window = tk.Toplevel()
    window.title(f"{action.capitalize()} Book")

    tk.Label(window, text="Title").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()

    tk.Label(window, text="Author").pack()
    author_entry = tk.Entry(window)
    author_entry.pack()

    # Additional fields for adding books
    if action == "add":
        tk.Label(window, text="Category").pack()
        category_entry = tk.Entry(window)
        category_entry.pack()

        tk.Label(window, text="Year").pack()
        year_entry = tk.Entry(window)
        year_entry.pack()

        tk.Label(window, text="Copies").pack()
        copies_entry = tk.Entry(window)
        copies_entry.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    def handle_action():
        title = title_entry.get().strip()
        author = author_entry.get().strip()

        if not title or not author:
            result_label.config(text="Title and author are required!", fg="red")
            return

        if action == "add":
            category = category_entry.get().strip()
            year = year_entry.get().strip()
            copies = copies_entry.get().strip()

            if not category or not year or not copies:
                result_label.config(text="All fields are required for adding a book!", fg="red")
                return

            # Add a new book to the DataFrame
            new_book = pd.DataFrame({
                "title": [title],
                "author": [author],
                "genre": [category],
                "year": [int(year)],
                "copies": [int(copies)],
                "is_loaned": ["{}"],
                "borrow_count": [0],
                "waiting_list": ["[]"],
                "available": [int(copies)],
                "popularity_score": [0]
            })
            global books_df
            books_df = pd.concat([books_df, new_book], ignore_index=True)
            save_books_to_file(books_df, BOOKS_FILE)
            log_info(f"Book '{title}' added successfully.")
            log_text.insert("end", f"Book '{title}' added successfully.\n")
            result_label.config(text="Book added successfully!", fg="green")

        elif action == "remove":
            book_index = books_df[(books_df["title"] == title) & (books_df["author"] == author)].index
            if not book_index.empty:
                books_df.drop(book_index, inplace=True)
                save_books_to_file(books_df, BOOKS_FILE)
                log_info(f"Book '{title}' removed successfully.")
                log_text.insert("end", f"Book '{title}' removed successfully.\n")
                result_label.config(text="Book removed successfully!", fg="green")
            else:
                log_error(f"Book '{title}' by {author} not found.")
                log_text.insert("end", f"Book '{title}' not found.\n")
                result_label.config(text="Book not found!", fg="red")

        elif action == "lend":
            book = books_df[(books_df["title"] == title) & (books_df["author"] == author)]
            if not book.empty and book.iloc[0]["available"] > 0:
                books_df.loc[book.index, "available"] -= 1
                books_df.loc[book.index, "borrow_count"] += 1
                save_books_to_file(books_df, BOOKS_FILE)
                log_info(f"Book '{title}' lent successfully.")
                log_text.insert("end", f"Book '{title}' lent successfully.\n")
                result_label.config(text="Book lent successfully!", fg="green")
            else:
                log_error(f"Book '{title}' unavailable for lending.")
                log_text.insert("end", f"Book '{title}' unavailable.\n")
                result_label.config(text="Book unavailable!", fg="red")

        elif action == "return":
            book = books_df[(books_df["title"] == title) & (books_df["author"] == author)]
            if not book.empty:
                books_df.loc[book.index, "available"] += 1
                save_books_to_file(books_df, BOOKS_FILE)
                log_info(f"Book '{title}' returned successfully.")
                log_text.insert("end", f"Book '{title}' returned successfully.\n")
                result_label.config(text="Book returned successfully!", fg="green")
            else:
                log_error(f"Book '{title}' not found for returning.")
                log_text.insert("end", f"Book '{title}' not found.\n")
                result_label.config(text="Book not found!", fg="red")

    tk.Button(window, text=action.capitalize() + " Book", command=handle_action).pack(pady=10)
