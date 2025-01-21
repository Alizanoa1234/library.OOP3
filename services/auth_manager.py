from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from models.user import User
from logs.actions import log_error, log_info

class AuthManager:
    def __init__(self, users_file: str):
        """
        Initialize the AuthManager, ensuring the users file exists.
        """
        self.users_file = users_file
        self.current_user = None
        self._initialize_users_file()

    def _initialize_users_file(self):
        """
        Ensures that the users.csv file exists with proper headers.
        If the file does not exist or is malformed, it creates it with default headers.
        """
        try:
            df = pd.read_csv(self.users_file)
            if not {'username', 'password'}.issubset(df.columns):
                raise ValueError("Malformed users file: Missing required columns.")
            log_info(f"Users file '{self.users_file}' loaded successfully.")

        except (FileNotFoundError, ValueError):
            # Create a new file with default headers
            df = pd.DataFrame(columns=['username', 'password'])
            df.to_csv(self.users_file, index=False)
            log_info(f"Users file '{self.users_file}' created or fixed with default headers.")

    def register_librarian(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register a new librarian with a hashed password.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password of the librarian.

        Returns:
            tuple: (bool, str) indicating success or failure and a message.
        """
        if not self.is_valid_username(username) or not self.is_valid_password(password):
            return False, "Invalid username or password"

        try:
            df = pd.read_csv(self.users_file)
            if username in df['username'].values:
                log_error(f"Registration failed: Username '{username}' already exists.")
                return False, "Username already exists"

            # Create a User object and store it
            user = User(username=username, password=password)
            df = pd.concat([df, pd.DataFrame([user.to_dict()])], ignore_index=True)
            df.to_csv(self.users_file, index=False)
            log_info(f"Librarian '{username}' registered successfully.")
            return True, "Librarian registered successfully"

        except Exception as e:
            log_error(f"Error registering librarian '{username}': {e}")
            return False, f"Error: {e}"

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a librarian using their username and password.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password of the librarian.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            df = pd.read_csv(self.users_file)
            user_row = df.loc[df['username'] == username]

            if not user_row.empty:
                stored_password = user_row.iloc[0]['password']
                if check_password_hash(stored_password, password):
                    self.current_user = username
                    log_info(f"Authentication successful for librarian '{username}'.")
                    return True
                else:
                    log_error(f"Authentication failed for librarian '{username}': Incorrect password.")
            else:
                log_error(f"Authentication failed for librarian '{username}': Username not found.")

        except FileNotFoundError:
            self._initialize_users_file()
            log_error(f"Users file '{self.users_file}' not found during authentication.")
        except Exception as e:
            log_error(f"Error authenticating librarian '{username}': {e}")

        return False

    def logout(self):
        """
        Logs out the currently logged-in librarian.
        """
        if self.current_user:
            log_info(f"User '{self.current_user}' logged out successfully.")
            self.current_user = None

    def is_valid_username(self, username: str) -> bool:
        """
        Validate the format of a username.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not username.strip():
            log_error("Username cannot be empty.")
            return False
        if not username.replace("_", "").isalnum():  # Allow underscores
            log_error(f"Username validation failed: '{username}' contains invalid characters.")
            return False
        return True

    def is_valid_password(self, password: str) -> bool:
        """
        Validate the format of a password.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if len(password) < 6:
            log_error("Password must be at least 6 characters long.")
            return False
        return True
