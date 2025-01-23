import tkinter as tk
from books_gui import open_books_gui
from search_gui import open_search_gui
from user_gui import open_user_gui
from logs.actions import log_info, TkinterLogHandler
import logging

# Configure the logger
logger = logging.getLogger("LibraryManagement")

def open_main_gui():
    root = tk.Tk()
    root.title("Library Management System")

    # Add heading
    tk.Label(root, text="Library Management System", font=("Arial", 16)).pack(pady=10)

    # Main buttons for all functionalities
    tk.Button(root, text="Add Book", command=lambda: open_books_gui(log_text, action="add")).pack(pady=5)
    tk.Button(root, text="Remove Book", command=lambda: open_books_gui(log_text, action="remove")).pack(pady=5)
    tk.Button(root, text="Search Book", command=lambda: open_search_gui(log_text, search_type="search")).pack(pady=5)
    tk.Button(root, text="View Books", command=lambda: open_search_gui(log_text, search_type="view")).pack(pady=5)
    tk.Button(root, text="Lend Book", command=lambda: open_books_gui(log_text, action="lend")).pack(pady=5)
    tk.Button(root, text="Return Book", command=lambda: open_books_gui(log_text, action="return")).pack(pady=5)
    tk.Button(root, text="Popular Books", command=lambda: open_search_gui(log_text, search_type="popular")).pack(pady=5)
    tk.Button(root, text="Login", command=lambda: open_user_gui(log_text, action="login")).pack(pady=5)
    tk.Button(root, text="Register", command=lambda: open_user_gui(log_text, action="register")).pack(pady=5)
    tk.Button(root, text="Logout", command=lambda: log_text.insert("end", "Logout successful.\n")).pack(pady=5)

    # Log display area
    log_frame = tk.LabelFrame(root, text="Logs", padx=10, pady=10)
    log_frame.pack(side="bottom", fill="both", expand=True)
    log_text = tk.Text(log_frame, wrap="word", height=10, state="normal")
    log_text.pack(fill="both", expand=True)

    # Attach custom log handler to logger
    log_handler = TkinterLogHandler(log_text)
    log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(log_handler)

    # Log system start
    log_info("Library Management System started.")

    root.mainloop()


if __name__ == "__main__":
    open_main_gui()
