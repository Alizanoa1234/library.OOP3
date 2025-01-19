import hashlib
import pandas as pd
from logs.actions import log_error, log_info

class AuthManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.current_user = None
        self.librarians = self.load_librarians(users_file)

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def load_librarians(self, file_path: str) -> dict:
        try:
            df = pd.read_csv(file_path)
            if "username" not in df.columns or "password_hash" not in df.columns:
                log_error(f"Invalid file format: {file_path}")
                return {}
            librarians = pd.Series(df.password_hash.values, index=df.username).to_dict()
            log_info(f"Librarians loaded from {file_path}.")
            return librarians
        except FileNotFoundError:
            log_error(f"Error: {file_path} not found.")
            return {}
        except Exception as e:
            log_error(f"Error loading librarians from {file_path}: {e}")
            return {}

    def register_librarian(self, username: str, password: str) -> tuple[bool, str]:
        if not self.is_valid_username(username) or not self.is_valid_password(password):
            return False, "Invalid username or password"

        if username in self.librarians:
            log_error(f"Registration failed: Username '{username}' already exists.")
            return False, "Username already exists"

        password_hash = self.hash_password(password)
        self.librarians[username] = password_hash
        self.save_librarians()
        log_info(f"Librarian '{username}' registered successfully.")
        return True, "Librarian registered successfully"

    def is_librarian_exists(self, username: str) -> bool:
        return username in self.librarians

    def is_valid_username(self, username: str) -> bool:
        if not username.strip():
            log_error("Username cannot be empty.")
            return False
        if not username.replace("_", "").isalnum():  # Allow underscores
            log_error(f"Username validation failed: '{username}' contains invalid characters.")
            return False
        return True

    def is_valid_password(self, password: str) -> bool:
        if len(password) < 6:
            log_error("Password must be at least 6 characters long.")
            return False
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self.librarians:
            log_error(f"Failed login attempt for username '{username}'.")
            return False
        if self.hash_password(password) != self.librarians[username]:
            log_error(f"Failed login attempt for username '{username}': Incorrect password.")
            return False
        self.current_user = username
        log_info(f"User '{username}' logged in successfully.")
        return True

    def logout(self):
        if self.current_user:
            log_info(f"User '{self.current_user}' logged out.")
            self.current_user = None

    def save_librarians(self):
        try:
            df = pd.DataFrame(list(self.librarians.items()), columns=["username", "password_hash"])
            df.to_csv(self.users_file, index=False)
            log_info(f"Librarians saved to {self.users_file}.")
        except Exception as e:
            log_error(f"Error saving librarians to {self.users_file}: {e}")
