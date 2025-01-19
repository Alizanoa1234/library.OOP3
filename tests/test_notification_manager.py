import unittest
from services.notification_manager import NotificationManager
from unittest.mock import patch


class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        """
        Set up a list of users and initialize the NotificationManager.
        """
        self.users = [
            {"name": "User1", "email": "user1@example.com"},
            {"name": "User2", "email": "user2@example.com"}
        ]
        self.notification_manager = NotificationManager(self.users)

    @patch("services.notification_manager.log_info")
    def test_notify_all(self, mock_log_info):
        """
        Test sending notifications to all users.
        """
        message = "New book added to the library."
        self.notification_manager.notify_all(message)

        # Verify that the notification was sent to all users
        self.assertEqual(mock_log_info.call_count, len(self.users) + 1)  # +1 for the broadcast log
        mock_log_info.assert_any_call(f"Broadcasting notification: {message}")
        for user in self.users:
            mock_log_info.assert_any_call(f"Notification sent to {user['name']} ({user['email']}): {message}")

    @patch("services.notification_manager.log_info")
    def test_send_notification(self, mock_log_info):
        """
        Test sending a single notification to a specific user.
        """
        user = self.users[0]
        message = "Test notification message."
        self.notification_manager._send_notification(user, message)

        # Verify that the notification log was called correctly
        mock_log_info.assert_called_once_with(f"Notification sent to {user['name']} ({user['email']}): {message}")


if __name__ == "__main__":
    unittest.main()
