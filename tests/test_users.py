import unittest
import os
import pandas as pd
from werkzeug.security import generate_password_hash
from data.users import UsersManager


class TestUsersManager(unittest.TestCase):
    TEST_FILE = "test_users.csv"

    def setUp(self):
        """
        Set up a temporary users file for testing and initialize UsersManager.
        """
        self.users_data = pd.DataFrame(columns=["username", "password"])
        self.users_data.to_csv(self.TEST_FILE, index=False)

        # Override USERS_FILE for testing
        UsersManager.USERS_FILE = self.TEST_FILE
        self.users_manager = UsersManager()

    def tearDown(self):
        """
        Remove the temporary test file after each test.
        """
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_register_librarian_success(self):
        """
        Test successful registration of a new librarian.
        """
        result, message = self.users_manager.register_librarian("new_user", "securepassword")
        self.assertTrue(result)
        self.assertEqual(message, "Librarian registered successfully")

        # Verify the new user exists in the file
        df = pd.read_csv(self.TEST_FILE)
        self.assertIn("new_user", df["username"].values)

    def test_register_existing_librarian(self):
        """
        Test registration of a librarian with an already existing username.
        """
        self.users_manager.register_librarian("existing_user", "password123")
        result, message = self.users_manager.register_librarian("existing_user", "newpassword")
        self.assertFalse(result)
        self.assertEqual(message, "Username already exists")

    def test_is_librarian_exists(self):
        """
        Test checking if a librarian exists.
        """
        self.users_manager.register_librarian("existing_user", "password123")
        self.assertTrue(self.users_manager.is_librarian_exists("existing_user"))
        self.assertFalse(self.users_manager.is_librarian_exists("nonexistent_user"))

    def test_authenticate_librarian_success(self):
        """
        Test successful authentication of a librarian.
        """
        self.users_manager.register_librarian("user1", "mypassword")
        self.assertTrue(self.users_manager.authenticate_librarian("user1", "mypassword"))

    def test_authenticate_librarian_incorrect_password(self):
        """
        Test authentication failure due to incorrect password.
        """
        self.users_manager.register_librarian("user1", "mypassword")
        self.assertFalse(self.users_manager.authenticate_librarian("user1", "wrongpassword"))

    def test_authenticate_librarian_nonexistent_user(self):
        """
        Test authentication failure for a non-existent user.
        """
        self.assertFalse(self.users_manager.authenticate_librarian("nonexistent_user", "password123"))


if __name__ == "__main__":
    unittest.main()
