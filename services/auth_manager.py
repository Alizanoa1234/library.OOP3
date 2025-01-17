import hashlib
import csv
from logs.actions import log_error, log_info

class AuthManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.current_user = None
        self.librarians = self.load_librarians(users_file)

    # Hashes a password using SHA-256
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # Loads librarian data from the CSV
    def load_librarians(self, file_path: str) -> dict:
        librarians = {}
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    librarians[row["username"]] = row["password_hash"]
                    log_info(f"Loaded librarians from {file_path}.")
        except FileNotFoundError:
            log_error(f"Error: {file_path} not found.")
        return librarians

    # Registers a new librarian
    def register_librarian(self, username: str, password: str) -> bool:

        if not self.is_valid_username(username) or not self.is_valid_password(password):
            return False

        if username in self.librarians:
            print(f"Username '{username}' already exists.")
            log_error(f"Registration failed: Username '{username}' already exists.")
            return False
        password_hash = self.hash_password(password)
        self.librarians[username] = password_hash
        self.save_librarians()
        log_info(f"Librarian '{username}' registered successfully.")
        return True

    def is_valid_username(self, username: str) -> bool:
        if not username.strip():
            log_error("Username cannot be empty.")
            return False
        if not username.isalnum():
            log_error("Username can only contain letters and numbers.")
            return False
        return True

    def is_valid_password(self, password: str) -> bool:
        if len(password) < 6:
            log_error("Password must be at least 6 characters long.")
            return False
        return True

    # Logs in a librarian
    def login(self, username: str, password: str) -> bool:
        if username not in self.librarians:
            print("Invalid username.")
            log_error(f"Failed login attempt for username '{username}'.")
            return False
        if self.hash_password(password) != self.librarians[username]:
            print("Incorrect password.")
            log_error(f"Failed login attempt for username '{username}'. Incorrect password.")
            return False
        self.current_user = username
        print(f"{username} logged in successfully.")
        log_info(f"User '{username}' logged in successfully.")
        return True

    # Logs out the current user
    def logout(self):
        if self.current_user:
            log_info(f"User '{self.current_user}' logged out.")
            print(f"{self.current_user} logged out.")
            self.current_user = None

    # Saves the updated librarians list to the CSV
    def save_librarians(self):
        try:
            with open(self.users_file, "w", newline="") as file:
                fieldnames = ["username", "password_hash"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for username, password_hash in self.librarians.items():
                    writer.writerow({"username": username, "password_hash": password_hash})
            log_info(f"Librarians saved to {self.users_file}.")

        except Exception as e:
            log_error(f"Error saving librarians to {self.users_file}: {e}")
