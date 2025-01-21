class Book:
    def __init__(self, title, author, category, year, copies, is_loaned_status="no"):
        self.title = title
        self.author = author
        self.category = category
        self.year = year
        self.copies = copies

        # Initialize the is_loaned dictionary for all copies
        self.is_loaned = {i + 1: is_loaned_status for i in range(copies)}

        # Calculate borrow_count based on initial is_loaned_status
        self.borrow_count = sum(1 for status in self.is_loaned.values() if status == "yes")

        # Calculate the available copies based on is_loaned
        self.available = sum(1 for status in self.is_loaned.values() if status == "no")

        # Initialize the waiting list and popularity score
        self.waiting_list = []
        self.popularity_score = self.borrow_count + len(self.waiting_list)

    def borrow(self, user_id: str):
        """
        Borrow a copy of the book or add to the waiting list.

        Args:
            user_id (str): The ID of the user borrowing the book.
        """
        for copy_id, status in self.is_loaned.items():
            if status == "no":
                self.is_loaned[copy_id] = "yes"
                self.borrow_count += 1
                self.popularity_score = self.borrow_count + len(self.waiting_list)
                return f"Copy {copy_id} loaned successfully."

        self.waiting_list.append(user_id)
        self.popularity_score = self.borrow_count + len(self.waiting_list)
        return "Added to waiting list."

    def return_copy(self, copy_id: int):
        """
        Return a borrowed copy.

        Args:
            copy_id (int): The ID of the copy being returned.
        """
        if self.is_loaned.get(copy_id) == "yes":
            self.is_loaned[copy_id] = "no"
            return f"Copy {copy_id} returned successfully."

        return f"Copy {copy_id} was not loaned."

    def to_dict(self):
        """
        Convert the book object to a dictionary.
        """
        return {
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "year": self.year,
            "copies": self.copies,
            "borrow_count": self.borrow_count,
            "is_loaned": self.is_loaned,
            "waiting_list": self.waiting_list,
            "popularity_score": self.popularity_score,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Book instance from a dictionary.
        """
        book = cls(
            title=data["title"],
            author=data["author"],
            category=data["category"],
            year=data["year"],
            copies=data["copies"],
        )
        book.borrow_count = data["borrow_count"]
        book.is_loaned = data["is_loaned"]
        book.waiting_list = data["waiting_list"]
        book.popularity_score = data["popularity_score"]
        return book
    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Copies: {self.copies}, "
                f"Available: {self.available}, Loaned: {self.is_loaned}, Genre: {self.category}, Year: {self.year}")

#FIXME לבדוק האם הפונקציות קיימות במקומות אחרים- זה לא המקום שלהם
##################################################################################
    #
    # def add_loaned_copy(self):
    #     """
    #     Marks the first available copy as loaned and updates availability.
    #
    #     Returns:
    #         int: The ID of the copy that was loaned, or None if no copy was available.
    #     """
    #     if self.available == 0:
    #         #FIXME- אך לדעת את מי להוסיף
    #         self.waiting_list.append(user_id)
    #         print(f"User {user_id} added to the waiting list for '{self.title}'.")
    #         # Update the DataFrame with the new waiting list
    #         data_frame.loc[data_frame['title'] == self.title, 'waiting_list'] = [self.waiting_list]
    #         return "added_to_waiting_list"
    #
    #     # Find the first available copy
    #     for copy_id, status in self.is_loaned.items():
    #         if status == "no":  # Copy is available
    #             self.is_loaned[copy_id] = "yes"
    #             self.available -= 1
    #             self.borrow_count += 1
    #
    #             # Update the DataFrame
    #             data_frame.loc[data_frame['title'] == self.title, 'is_loaned'] = [self.is_loaned]
    #             data_frame.loc[data_frame['title'] == self.title, 'available'] = self.available
    #             data_frame.loc[data_frame['title'] == self.title, 'borrow_count'] = self.borrow_count
    #
    #             print(f"Book '{self.title}', Copy ID {copy_id} loaned successfully.")
    #             return f"Book '{self.title}' loaned successfully. (Copy ID: {copy_id})"
    #
    #     # Fallback in case something unexpected happens
    #     print("No available copies found (unexpected).")
    #     return None
    #
    # def return_loaned_copy(self):
    #     """
    #     Marks the first loaned copy as returned and updates availability.
    #
    #     This method automatically returns the first loaned copy (copy with status "yes").
    #     """
    #     # Find the first loaned copy (status == "yes")
    #     for copy_id, status in self.is_loaned.items():
    #         if status == "yes":  # First loaned copy found
    #             self.is_loaned[copy_id] = "no"
    #             self.available += 1
    #             print(f"Book '{self.title}', Copy ID {copy_id} returned successfully.")
    #             return  # Exit the method after returning the first copy
    #
    #     # If no loaned copy was found, print a message
    #     print(f"No loaned copies found for book '{self.title}'.")
    #
    # def available_copies_count(self):
    #     """
    #     Returns the number of available copies for this book.
    #
    #     Returns:
    #         int: The number of available copies.
    #     """
    #     return sum(1 for status in self.is_loaned.values() if status == "no")
    #
    # def has_available_copy(self):
    #     """
    #     Checks if there is at least one available copy of the book.
    #
    #     Returns:
    #         bool: True if at least one copy is available, False otherwise.
    #     """
    #     return self.available_copies_count() > 0
    #
    # def add_to_waiting_list(self, user_id):
    #     """
    #     Adds a user to the waiting list if no copies are available.
    #
    #     Args:
    #         user_id (str): The unique identifier of the user.
    #     """
    #     if not self.has_available_copy():
    #         self.waiting_list.append(user_id)
    #         print(f"User {user_id} added to waiting list.")
    #     else:
    #         print("There is an available copy. No need to wait.")
    #
    # def remove_from_waiting_list(self, user_id):
    #     """
    #     Removes a user from the waiting list.
    #
    #     Args:
    #         user_id (str): The unique identifier of the user.
    #     """
    #     if user_id in self.waiting_list:
    #         self.waiting_list.remove(user_id)
    #         print(f"User {user_id} removed from waiting list.")
    #     else:
    #         print(f"User {user_id} is not on the waiting list.")
