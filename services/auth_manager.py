import hashlib
import pandas as pd
from logs.actions import log_error, log_info

class AuthManager:
    def _init_(self, users_file: str):
        self.users_file = users_file
        self.current_user = None
        self.librarians = self.load_librarians(users_file)

    # Hashes a password using SHA-256
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # Loads librarian data from the CSV using pandas
    def load_librarians(self, file_path: str) -> dict:
        """
        Loads librarians from the CSV into a dictionary.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            dict: A dictionary of usernames and hashed passwords.
        """
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

    # Registers a new librarian
    def register_librarian(self, username: str, password: str) -> bool:
        """
        Registers a new librarian.

        Args:
            username (str): Username of the librarian.
            password (str): Password of the librarian.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
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
        """
        Validates a username.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if the username is valid, False otherwise.
        """
        if not username.strip():
            log_error("Username cannot be empty.")
            return False
        if not username.isalnum():
            log_error("Username can only contain letters and numbers.")
            return False
        return True

    def is_valid_password(self, password: str) -> bool:
        """
        Validates a password.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if len(password) < 6:
            log_error("Password must be at least 6 characters long.")
            return False
        return True

    # Logs in a librarian
    def login(self, username: str, password: str) -> bool:
        """
        Logs in a librarian.

        Args:
            username (str): Username of the librarian.
            password (str): Password of the librarian.

        Returns:
            bool: True if login is successful, False otherwise.
        """
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
        """
        Logs out the current user.
        """
        if self.current_user:
            log_info(f"User '{self.current_user}' logged out.")
            print(f"{self.current_user} logged out.")
            self.current_user = None

    # Saves the updated librarians list to the CSV using pandas
    def save_librarians(self):
        """
        Saves the librarian data to the CSV file.
        """
        try:
            df = pd.DataFrame(list(self.librarians.items()), columns=["username", "password_hash"])
            df.to_csv(self.users_file, index=False)
            log_info(f"Librarians saved to {self.users_file}.")
        except Exception as e:
            log_error(f"Error saving librarians to {self.users_file}: {e}")