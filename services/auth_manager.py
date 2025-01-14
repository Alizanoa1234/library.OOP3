import hashlib
import csv

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
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        return librarians

    # Registers a new librarian
    def register_librarian(self, username: str, password: str) -> bool:
        if username in self.librarians:
            print(f"Username '{username}' already exists.")
            return False
        password_hash = self.hash_password(password)
        self.librarians[username] = password_hash
        self.save_librarians()
        return True

    # Logs in a librarian
    def login(self, username: str, password: str) -> bool:
        if username not in self.librarians:
            print("Invalid username.")
            return False
        if self.hash_password(password) != self.librarians[username]:
            print("Incorrect password.")
            return False
        self.current_user = username
        print(f"{username} logged in successfully.")
        return True

    # Logs out the current user
    def logout(self):
        if self.current_user:
            print(f"{self.current_user} logged out.")
            self.current_user = None

    # Saves the updated librarians list to the CSV
    def save_librarians(self):
        with open(self.users_file, "w", newline="") as file:
            fieldnames = ["username", "password_hash"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for username, password_hash in self.librarians.items():
                writer.writerow({"username": username, "password_hash": password_hash})
