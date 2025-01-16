import uuid

class Book:
    def __init__(self, title, author, category, year, copies):
        """
        Initializes a Book object.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            category (str): The category/genre of the book.
            year (int): The publication year of the book.
            copies (int): The total number of copies of the book available.
        """
        self.book_id = uuid.uuid4()  # Unique identifier for the book
        self.title = title
        self.author = author
        self.category = category
        self.year = year
        self.copies = copies
        self.is_loaned = {}  # Dictionary tracking the loan status of each copy
        self.available = copies  # Number of available copies
        self.borrow_count = 0  # Number of times the book has been borrowed
        self.waiting_list = []  # List of users waiting for the book

    def __str__(self):
        """
        Return a readable string representation of the Book object.
        """
        is_loaned_str = ', '.join(
            [f" {index}: {status}" for index, (copy_id, status) in enumerate(self.is_loaned.items(), start=1)])
        return f"title: {self.title}, author: {self.author}, copies: {self.copies}, is_loaned: {is_loaned_str}, genre: {self.category}, year: {self.year}"

    def add_loaned_copy(self, copy_id):
        """
        Marks a copy as loaned and updates availability.

        Args:
            copy_id (int): The ID of the copy being loaned.
        """
        self.is_loaned[copy_id] = "yes"
        self.available -= 1
        self.borrow_count += 1

    def return_loaned_copy(self, copy_id):
        """
        Marks a loaned copy as returned and updates availability.

        Args:
            copy_id (int): The ID of the copy being returned.
        """
        if copy_id in self.is_loaned and self.is_loaned[copy_id] == "yes":
            self.is_loaned[copy_id] = "no"
            self.available += 1

    def available_copies_count(self):
        """
        Returns the number of available copies for this book.

        Returns:
            int: The number of available copies.
        """
        return sum(1 for status in self.is_loaned.values() if status == "no")

    def has_available_copy(self):
        """
        Checks if there is at least one available copy of the book.

        Returns:
            bool: True if at least one copy is available, False otherwise.
        """
        return self.available_copies_count() > 0

    def add_to_waiting_list(self, user_id):
        """
        Adds a user to the waiting list if no copies are available.

        Args:
            user_id (str): The unique identifier of the user.
        """
        if not self.has_available_copy():
            self.waiting_list.append(user_id)
            print(f"User {user_id} added to waiting list.")
        else:
            print("There is an available copy. No need to wait.")

    def remove_from_waiting_list(self, user_id):
        """
        Removes a user from the waiting list.

        Args:
            user_id (str): The unique identifier of the user.
        """
        if user_id in self.waiting_list:
            self.waiting_list.remove(user_id)
            print(f"User {user_id} removed from waiting list.")
        else:
            print(f"User {user_id} is not on the waiting list.")
