class BookDecorator:
    """
    A decorator for the Book class that tracks the book's popularity
    based on the number of times it has been borrowed.
    """

    def __init__(self, book):
        """
        Initializes the BookDecorator with a Book object.

        Args:
            book (Book): The book object to decorate.
        """
        self.book = book
        self.borrow_count = 0  # Tracks how many times the book has been borrowed.

    def increase_borrow_count(self):
        """
        Increases the borrow count by 1.
        """
        self.borrow_count += 1

    def get_borrow_count(self) -> int:
        """
        Returns the number of times the book has been borrowed.

        Returns:
            int: The borrow count.
        """
        return self.borrow_count

    def __getattr__(self, name):
        """
        Delegates attribute access to the wrapped book object.

        Args:
            name (str): The attribute name.

        Returns:
            Any: The attribute or method from the original Book object.
        """
        return getattr(self.book, name)

    def __str__(self) -> str:
        """
        Returns a string representation of the decorated book, including its borrow count.

        Returns:
            str: A string with the book's details and borrow count.
        """
        return f"{str(self.book)} | Borrow Count: {self.borrow_count}"
