from logs.actions import log_info


class NotificationManager:
    """
    Handles notifications to all users when events occur in the library system.
    """

    def _init_(self, users: list):
        """
        Initializes the NotificationManager with a list of users.

        Args:
            users (list): A list of dictionaries representing users. Each user has 'name' and 'email' fields.
        """
        self.users = users  # List of users to notify (e.g., [{'name': 'Librarian1', 'email': 'lib1@example.com'}, ...])

    def notify_all(self, message: str):
        """
        Sends a notification message to all users.

        Args:
            message (str): The notification message.
        """
        log_info(f"Broadcasting notification: {message}")
        for user in self.users:
            self._send_notification(user, message)

    def _send_notification(self, user: dict, message: str):
        """
        Simulates sending a notification to a user.

        Args:
            user (dict): A dictionary containing 'name' and 'email' of the user.
            message (str): The notification message.
        """
        # Simulate sending an email or other notification
        print(f"Notification sent to {user['name']} ({user['email']}): {message}")
        log_info(f"Notification sent to {user['name']} ({user['email']}): {message}")