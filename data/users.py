import csv
from werkzeug.security import generate_password_hash, check_password_hash

class LibrarianManager:
    """
    A class to manage librarian users in the library system.
    Handles librarian registration, authentication, and user management.
    """

    USERS_FILE = 'data/users.csv'

    def __init__(self):
        """
        Initialize the librarian manager and ensure the users file exists.
        """
        self._initialize_users_file()

    def _initialize_users_file(self):
        """
        Ensures that the users.csv file exists with proper headers.
        If the file does not exist, it creates it with default headers.
        """
        try:
            with open(self.USERS_FILE, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password'])  # File headers
        except FileExistsError:
            pass  # File already exists, no need to initialize again

    def register_librarian(self, username, password):
        """
        Register a new librarian with a hashed password.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password of the librarian.

        Returns:
            tuple: (bool, str) indicating success or failure and a message.
        """
        hashed_password = generate_password_hash(password)

        if self.is_librarian_exists(username):
            return False, "Username already exists"

        # Append the librarian's credentials to the file
        with open(self.USERS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])
        return True, "Librarian registered successfully"

    def is_librarian_exists(self, username):
        """
        Check if a librarian with the given username exists in the system.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the librarian exists, False otherwise.
        """
        try:
            with open(self.USERS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the headers
                for row in reader:
                    if row[0] == username:
                        return True
        except FileNotFoundError:
            self._initialize_users_file()
        return False

    def authenticate_librarian(self, username, password):
        """
        Authenticate a librarian using their username and password.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password of the librarian.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            with open(self.USERS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the headers
                for row in reader:
                    stored_username, stored_password = row
                    if username == stored_username and check_password_hash(stored_password, password):
                        return True
        except FileNotFoundError:
            self._initialize_users_file()
        return False
