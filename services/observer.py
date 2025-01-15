class Subscriber:
    """
    Represents a librarian who receives notifications about book availability.
    """

    def __init__(self, name: str, email: str):
        """
        Initializes a subscriber (librarian) who will receive notifications.
        Args:
            name (str): The librarian's name.
            email (str): The librarian's email.
        """
        self.name = name
        self.email = email

    def notify(self, message: str):
        """
        Sends a notification message to the librarian.
        Args:
            message (str): The notification message.
        """
        print(f"Notification sent to librarian {self.name} ({self.email}): {message}")


class ObserverManager:
    """
    Manages the list of subscribers (librarians) and sends notifications when books become available.
    """

    def __init__(self):
        """
        Initializes an empty dictionary to store subscribers.
        """
        self.subscribers = {}  # Maps book IDs to lists of subscribers (librarians)

    def add_subscriber(self, book_id: int, subscriber: Subscriber):
        """
        Adds a librarian to the waitlist for a specific book.
        Args:
            book_id (int): The ID of the book.
            subscriber (Subscriber): The librarian who will be notified.
        """
        if book_id not in self.subscribers:
            self.subscribers[book_id] = []
        self.subscribers[book_id].append(subscriber)
        print(f"Librarian {subscriber.name} added to the notification list for book ID {book_id}.")

    def remove_subscriber(self, book_id: int, email: str):
        """
        Removes a librarian from the waitlist for a specific book by their email.
        Args:
            book_id (int): The ID of the book.
            email (str): The email of the librarian to remove.
        """
        if book_id in self.subscribers:
            initial_count = len(self.subscribers[book_id])
            self.subscribers[book_id] = [sub for sub in self.subscribers[book_id] if sub.email != email]

            if len(self.subscribers[book_id]) < initial_count:
                print(f"Librarian with email {email} removed from the notification list for book ID {book_id}.")
            else:
                print(f"Librarian with email {email} not found in the notification list for book ID {book_id}.")
        else:
            print(f"No subscribers for book ID {book_id}.")

    def notify_librarians(self, book_id: int, book_title: str):
        """
        Sends notifications to librarians when a book becomes available.
        Args:
            book_id (int): The ID of the book that became available.
            book_title (str): The title of the book.
        """
        if book_id not in self.subscribers or not self.subscribers[book_id]:
            print(f"No librarians to notify for book ID {book_id}.")
            return

        message = f"The book '{book_title}' (ID: {book_id}) is now available and someone is on the waitlist."
        for subscriber in self.subscribers[book_id]:
            subscriber.notify(message)

        # Clear the waitlist after notifying
        self.subscribers[book_id] = []

    def clear_waitlist(self, book_id: int):
        """
        Clears all subscribers from the waitlist for a specific book.
        Args:
            book_id (int): The ID of the book.
        """
        if book_id in self.subscribers:
            self.subscribers[book_id] = []
            print(f"Waitlist cleared for book ID {book_id}.")
        else:
            print(f"No subscribers for book ID {book_id}.")
