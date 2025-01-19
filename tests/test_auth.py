import unittest
import os
import pandas as pd
from services.auth_manager import AuthManager

class TestAuthManager(unittest.TestCase):
    USERS_FILE = "test_users.csv"

    def setUp(self):
        """
        Set up a temporary users file and initialize AuthManager.
        """
        # Ensure the test file is used
        self.auth_manager = AuthManager(self.USERS_FILE)

        # Create a test users file with an admin user
        self.auth_manager.register_librarian("admin", "password123")
        try:
            df = pd.read_csv(self.USERS_FILE)
        except FileNotFoundError:
            print(f"{self.USERS_FILE} does not exist.")
    def tearDown(self):
        """
        Clean up the test users file after each test.
        """
        if os.path.exists(self.USERS_FILE):
            os.remove(self.USERS_FILE)

    def test_register_librarian(self):
        """
        Test registering a new librarian.
        """
        # Updated username to a valid alphanumeric one
        result, message = self.auth_manager.register_librarian("newLibrarian", "securepass")
        print(f"Test Register Librarian Result: {result}, Message: {message}")  # Debug log
        self.assertTrue(result)

        # Verify the librarian exists in the file
        df = pd.read_csv(self.USERS_FILE)
        self.assertIn("newLibrarian", df["username"].values)

    def test_register_existing_librarian(self):
        """
        Test registering a librarian with an existing username.
        """
        result, message = self.auth_manager.register_librarian("admin", "newpassword")
        self.assertFalse(result)
        self.assertEqual(message, "Username already exists")

    def test_is_librarian_exists(self):
        """
        Test checking if a librarian exists.
        """
        self.assertTrue(self.auth_manager.is_librarian_exists("admin"))
        self.assertFalse(self.auth_manager.is_librarian_exists("nonexistent"))

    def test_authenticate_librarian_success(self):
        """
        Test successful authentication of a librarian.
        """
        result = self.auth_manager.login("admin", "password123")
        self.assertTrue(result)

    def test_authenticate_librarian_fail_wrong_password(self):
        """
        Test authentication failure due to incorrect password.
        """
        result = self.auth_manager.login("admin", "wrongpass")
        self.assertFalse(result)

    def test_authenticate_librarian_fail_nonexistent_user(self):
        """
        Test authentication failure due to non-existent user.
        """
        result = self.auth_manager.login("nonexistent", "password123")
        self.assertFalse(result)

    def test_logout(self):
        """
        Test logging out a logged-in librarian.
        """
        self.auth_manager.login("admin", "password123")
        self.assertEqual(self.auth_manager.current_user, "admin")

        self.auth_manager.logout()
        self.assertIsNone(self.auth_manager.current_user)

if __name__ == "__main__":
    unittest.main()
