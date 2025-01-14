class BookIterator:
    """
    An iterator for navigating through a collection of books.
    """

    def __init__(self, books: list):
        """
        Initializes the iterator with a list of books.

        Args:
            books (list): The list of books to iterate over.
        """
        self.books = books
        self.index = 0

    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self

    def __next__(self):
        """
        Returns the next book in the collection.

        Raises:
            StopIteration: When there are no more books to iterate over.
        """
        if self.index >= len(self.books):
            raise StopIteration
        book = self.books[self.index]
        self.index += 1
        return book

    def reset(self):
        """
        Resets the iterator to the beginning of the book collection.
        """
        self.index = 0
