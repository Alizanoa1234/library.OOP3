import tkinter as tk
from tkinter import messagebox
from services.auth_manager import AuthManager
from logs.actions import log_info, log_error


class UserGUI:
    """
    Handles librarian login and registration GUI.
    """

    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("User Management")
        self.root.geometry("400x300")
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
        tk.Button(self.root, text="Back", command=self.root.destroy).pack(pady=10)

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

            if self.auth_manager.login(username, password):
                log_info(f"User '{username}' logged in successfully.")
                messagebox.showinfo("Success", "Logged in successfully!")
                self.create_main_menu()
            else:
                log_error(f"Failed login attempt for user '{username}'.")
                messagebox.showerror("Error", "Invalid username or password.")

        tk.Button(self.root, text="Login", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

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

            success, message = self.auth_manager.register_librarian(username, password)
            if success:
                log_info(f"User '{username}' registered successfully.")
                messagebox.showinfo("Success", "Registered successfully!")
                self.create_main_menu()
            else:
                log_error(f"Registration failed for user '{username}': {message}")
                messagebox.showerror("Error", message)

        tk.Button(self.root, text="Register", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

    def clear_screen(self):
        """
        Clears all widgets from the current screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
