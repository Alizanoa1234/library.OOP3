import pandas as pd
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
            # Check if the file exists, if not, create it with headers
            pd.read_csv(self.USERS_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['username', 'password'])
            df.to_csv(self.USERS_FILE, index=False)

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
        df = pd.read_csv(self.USERS_FILE)

        if username in df['username'].values:
            return False, "Username already exists"

        # Append the new librarian
        new_row = pd.DataFrame({'username': [username], 'password': [hashed_password]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.USERS_FILE, index=False)
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
            df = pd.read_csv(self.USERS_FILE)
            return username in df['username'].values
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
            df = pd.read_csv(self.USERS_FILE)
            user = df.loc[df['username'] == username]
            if not user.empty:
                stored_password = user.iloc[0]['password']
                return check_password_hash(stored_password, password)
        except FileNotFoundError:
            self._initialize_users_file()
        return False
