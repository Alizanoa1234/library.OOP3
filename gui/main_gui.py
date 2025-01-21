import tkinter as tk
from books_gui import BooksGUI
from search_gui import SearchGUI
from services.library_manager import LibraryManager
from user_gui import UserGUI
from logs.actions import log_info

class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.library_manager = LibraryManager("books.csv")
        self.root.geometry("400x400")
        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(self.root, text="Library Management System", font=("Helvetica", 16)).pack(pady=20)

        buttons = [
            ("Manage Books", lambda: BooksGUI(self.root)),
            ("Search Books", lambda: SearchGUI(self.root, library_manager=self.library_manager)),
            ("User Management", lambda: UserGUI(self.root)),
            ("Exit", self.exit_application)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, width=20, command=command).pack(pady=10)

    def exit_application(self):
        log_info("Application exited successfully.")
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainGUI()
    app.run()
