import tkinter as tk
from tkinter import messagebox
from services.library_manager import LibraryManager
from logs.actions import log_info, log_error

class BooksGUI:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Books Management")
        self.library_manager = LibraryManager("data/books.csv")
        self.create_books_menu()

    def create_books_menu(self):
        tk.Label(self.root, text="Manage Books", font=("Helvetica", 16)).pack(pady=20)

        buttons = [
            ("Add Book", self.add_book_screen),
            ("Remove Book", self.remove_book_screen),
            ("View Books", self.view_books_screen),
            ("Back", self.root.destroy)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, width=20, command=command).pack(pady=10)

    def add_book_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Book", font=("Helvetica", 14)).pack(pady=10)
        entries = {}
        for label in ["Title", "Author", "Year", "Category", "Copies"]:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[label.lower()] = entry

        def submit():
            try:
                from models.book import Book
                book = Book(
                    title=entries["title"].get(),
                    author=entries["author"].get(),
                    year=int(entries["year"].get()),
                    category=entries["category"].get(),
                    copies=int(entries["copies"].get())
                )
                if self.library_manager.add_book(book):
                    log_info(f"Book '{book.title}' added successfully.")
                    messagebox.showinfo("Success", "Book added successfully!")
                else:
                    log_error(f"Failed to add book '{book.title}'.")
                    messagebox.showerror("Error", "Failed to add book.")
            except Exception as e:
                log_error(f"Error adding book: {e}")
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Add", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_books_menu).pack(pady=5)

    def remove_book_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Remove Book", font=("Helvetica", 14)).pack(pady=10)
        title_entry = tk.Entry(self.root)
        tk.Label(self.root, text="Title").pack()
        title_entry.pack()
        author_entry = tk.Entry(self.root)
        tk.Label(self.root, text="Author").pack()
        author_entry.pack()

        def submit():
            if self.library_manager.remove_book(title_entry.get(), author_entry.get()):
                log_info(f"Book '{title_entry.get()}' removed successfully.")
                messagebox.showinfo("Success", "Book removed successfully!")
            else:
                log_error(f"Failed to remove book '{title_entry.get()}'.")
                messagebox.showerror("Error", "Failed to remove book.")

        tk.Button(self.root, text="Remove", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_books_menu).pack(pady=5)

    def view_books_screen(self):
        self.clear_screen()
        books = self.library_manager.get_all_books()
        tk.Label(self.root, text="Books", font=("Helvetica", 14)).pack(pady=10)
        text = tk.Text(self.root)
        text.pack()
        for book in books:
            text.insert("end", f"{book}\n")

        tk.Button(self.root, text="Back", command=self.create_books_menu).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
