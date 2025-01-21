import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from logs.actions import log_info, log_error
from models.user import User


class UsersManager:
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
        If the file does not exist or is malformed, it creates it with default headers.
        """
        try:
            # Check if the file exists and validate its structure
            df = pd.read_csv(self.USERS_FILE)
            if not {'username', 'password'}.issubset(df.columns):
                raise ValueError("Malformed users file: Missing required columns.")
            log_info(f"Users file '{self.USERS_FILE}' loaded successfully.")

        except (FileNotFoundError, ValueError) as e:
            # Create a new file with default headers
            df = pd.DataFrame(columns=['username', 'password'])
            df.to_csv(self.USERS_FILE, index=False)
            log_info(f"Users file '{self.USERS_FILE}' created or fixed with default headers.")

    def register_librarian(self, username, password):
        """
        Register a new librarian with a hashed password.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password of the librarian.

        Returns:
            tuple: (bool, str) indicating success or failure and a message.
        """
        # Validate username
        if not username.isalnum() or len(username) < 3:
            log_error(f"Registration failed: Invalid username '{username}'.")
            return False, "Invalid username. It must be at least 3 characters long and alphanumeric."

        df = pd.read_csv(self.USERS_FILE)
        if username in df['username'].values:
            log_error(f"Registration failed: Username '{username}' already exists.")
            return False, "Username already exists"

        # Create a User object and store it
        user = User(username=username, password=password)
        df = pd.concat([df, pd.DataFrame([user.to_dict()])], ignore_index=True)
        df.to_csv(self.USERS_FILE, index=False)
        log_info(f"Librarian '{username}' registered successfully.")
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
            exists = username in df['username'].values
            log_info(f"Checked existence for librarian '{username}': {'Exists' if exists else 'Does not exist'}.")
            return exists
        except FileNotFoundError:
            self._initialize_users_file()
            log_error(f"Users file '{self.USERS_FILE}' not found during existence check.")
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
                if check_password_hash(stored_password, password):
                     log_info(f"Authentication successful for librarian '{username}'.")
                     return True
                else:
                    log_error(f"Authentication failed for librarian '{username}': Incorrect password.")

            else:
                log_error(f"Authentication failed for librarian '{username}': Username not found.")

        except FileNotFoundError:
            self._initialize_users_file()
            log_error(f"Users file '{self.USERS_FILE}' not found during authentication.")
        return False