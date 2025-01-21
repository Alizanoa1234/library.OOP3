from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """
    Represents a librarian user in the library system.
    """

    def __init__(self, username: str, password: str, hashed: bool = False):
        """
        Initialize a user.

        Args:
            username (str): The username of the librarian.
            password (str): The plain text password or hashed password.
            hashed (bool): Indicates whether the provided password is already hashed.
        """
        self.username = username
        self._password = password if hashed else generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided plain text password matches the stored hashed password.

        Args:
            password (str): The plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self._password, password)

    def to_dict(self) -> dict:
        """
        Convert the user object to a dictionary for storage.

        Returns:
            dict: A dictionary representation of the user.
        """
        return {
            'username': self.username,
            'password': self._password,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a User instance from a dictionary.

        Args:
            data (dict): A dictionary containing the user's data.

        Returns:
            User: An instance of the User class.
        """
        return cls(username=data['username'], password=data['password'], hashed=True)
