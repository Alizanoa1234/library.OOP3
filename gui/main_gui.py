import tkinter as tk
from books_gui import open_books_gui
from search_gui import open_search_gui
from user_gui import open_user_gui
from logs.actions import log_info

def main_gui():
    root = tk.Tk()
    root.title("Library Management System")

    tk.Label(root, text="Library Management System", font=("Arial", 18, "bold")).pack(pady=10)

    # Buttons for different functionalities
    tk.Button(root, text="Add Book", command=lambda: open_books_gui("add")).pack(pady=5)
    tk.Button(root, text="Remove Book", command=lambda: open_books_gui("remove")).pack(pady=5)
    tk.Button(root, text="Search Book", command=open_search_gui).pack(pady=5)
    tk.Button(root, text="View Books", command=lambda: open_books_gui("view")).pack(pady=5)
    tk.Button(root, text="Lend Book", command=lambda: open_books_gui("lend")).pack(pady=5)
    tk.Button(root, text="Return Book", command=lambda: open_books_gui("return")).pack(pady=5)
    tk.Button(root, text="Login", command=lambda: open_user_gui("login")).pack(pady=5)
    tk.Button(root, text="Register", command=lambda: open_user_gui("register")).pack(pady=5)
    tk.Button(root, text="Popular Books", command=lambda: open_books_gui("popular")).pack(pady=5)
    tk.Button(root, text="Logout", command=lambda: log_info("User logged out successfully.")).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
