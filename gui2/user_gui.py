import tkinter as tk
from tkinter import messagebox

from gui2.books_gui import BooksGUI
from services.auth_manager import AuthManager
from logs.actions import log_info, log_error

class UserGUI:
    """
    Handles librarian login and registration GUI.
    """

    def __init__(self, root, on_success):
        """
        Initialize the user management GUI.

        Args:
            root (tk.Tk): The main application window.
            on_success (function): Callback to execute on successful login.
        """
        self.root = root  # Use the main root window
        self.on_success = on_success
        self.auth_manager = AuthManager("data/users.csv")
        self.create_main_menu()

    def create_main_menu(self):
        """
        Displays the main user menu with options for login and registration.
        """
        self.clear_screen()
        tk.Label(self.root, text="User Management", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self.root, text="Login", command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)

    def login_screen(self):
        """
        Displays the login screen.
        """
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Helvetica", 14)).pack(pady=10)

        # Username and password input
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Username and password cannot be empty.")
                return

            try:
                if self.auth_manager.login(username, password):
                    log_info(f"User '{username}' logged in successfully.")
                    messagebox.showinfo("Success", "Logged in successfully!")
                    self.root.destroy()  # Close login window
                    self.on_success()  # Callback to main application
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))  # Show specific error
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        tk.Button(self.root, text="Login", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: submit())

    def register_screen(self):
        """
        Displays the registration screen.
        """
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Helvetica", 14)).pack(pady=10)

        # Username and password input
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Username and password cannot be empty.")
                return

            success, message = self.auth_manager.register_librarian(username, password)
            if success:
                log_info(f"User '{username}' registered successfully.")
                messagebox.showinfo("Success", "Registered successfully!")
                self.create_main_menu()
            else:
                log_error(f"Registration failed for user '{username}': {message}")
                messagebox.showerror("Error", message)  # Display detailed error message

        tk.Button(self.root, text="Register", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: submit())

    def clear_screen(self):
        """
        Clears all widgets from the current screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        # Unbind Enter key to prevent duplicate bindings
        self.root.unbind('<Return>')

def on_login_success(root):
    """
    Callback function to open the Books Management system after successful login.
    """
    print("Login successful! Opening Books Management system...")

    # נשתמש בחלון הראשי שכבר קיים
    for widget in root.winfo_children():
        widget.destroy()  # הסרת כל הווידג'טים מהחלון הראשי

    BooksGUI(root, "C:/Users/sapir/PycharmProjects/library.OOP3/data/books.csv")


if __name__ == "__main__":

    root = tk.Tk()
    UserGUI(root, on_login_success(root))
    root.mainloop()
