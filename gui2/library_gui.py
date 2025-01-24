import tkinter as tk
from tkinter import messagebox

from gui2.books_gui import BooksGUI


class LibraryGUI:
    def __init__(self, root, csv_file):
        """
        Initialize the main Library GUI.

        Args:
            root (tk.Tk): The main Tkinter window.
            csv_file (str): Path to the CSV file for the library.
        """
        self.root = root
        self.root.title("Library Management System")
        self.csv_file = csv_file

        # Configure the main layout
        self.configure_layout()

    def configure_layout(self):
        """
        Configure the main layout of the Library GUI.
        """
        # Add buttons for different functionalities
        tk.Button(self.root, text="Manage Books", command=self.open_books_gui).pack(fill=tk.X, padx=10, pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(fill=tk.X, padx=10, pady=10)

    def open_books_gui(self):
        """
        Open the Books Management GUI.
        """
        new_window = tk.Toplevel(self.root)
        BooksGUI(new_window, self.csv_file)




if __name__ == "__main__":
    root = tk.Tk()
    gui = BooksGUI(root, "C:/Users/sapir/PycharmProjects/library.OOP3/data/books.csv")


    root.mainloop()
