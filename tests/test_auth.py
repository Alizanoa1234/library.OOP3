import unittest
from services.auth_manager import AuthManager

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.auth_manager = AuthManager()
        self.auth_manager.add_librarian("admin", "password123")

    def test_add_librarian(self):
        result = self.auth_manager.add_librarian("new_librarian", "securepass")
        self.assertTrue(result)
        self.assertIn("new_librarian", self.auth_manager.librarians)

    def test_authenticate_librarian_success(self):
        result = self.auth_manager.authenticate("admin", "password123")
        self.assertTrue(result)

    def test_authenticate_librarian_fail(self):
        result = self.auth_manager.authenticate("admin", "wrongpass")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
