from models.book import Book
# main.py

from data.books import load_books_from_file, save_books_to_file
from data.users import LibrarianManager
from models.book_iterator import BookIterator
from models.search_strategy import SearchManager, SearchByName


def main():
	#  Load books from the CSV file
	file_path = "books.csv"
	books  = load_books_from_file(file_path)

	# Print the books info before any action (without modifying anything)
	print("Books available before any action:")
	for book in books:
		print(book)
	# print("-" * 40)
	#
	# # Create a book object with initial data
	# book = Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 3, "no")
	# print("Initial book status:")
	# print(book)
	#
	# print("-" * 40)
	# print("Borrowing copies:")
	# for _ in range(4):  # Try borrowing 4 times (one extra to trigger waitlist)
	# 	copy_id = book.add_loaned_copy()
	# 	if copy_id is None:
	# 		print("No available copies. Adding user to the waiting list.")
	# 		book.add_to_waiting_list(f"user_{_ + 1}")
	# print("-" * 40)
	#
	# # Check how many copies are available
	# print(f"Available copies: {book.available_copies_count()}")
	# print("-" * 40)
	#
	# # Simulate returning a copy
	# print("Returning a copy:")
	# book.return_loaned_copy(1)  # Return the first copy
	# print(f"Available copies after return: {book.available_copies_count()}")
	# print("-" * 40)
	#
	# # Simulate borrowing again and check waiting list
	# print("Borrowing after return:")
	# book.add_loaned_copy()
	# print("Waiting list:", book.waiting_list)
	# print("-" * 40)
	#
	# # Final book status
	# print("Final book status:")
	# print(book)

	# book = Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 3, "no")
	#
	# print("Initial book status:")
	# print(book)  # הדפסת מצב הספר
	#
	# # השאלת ספר
	# book.add_loaned_copy()
	# book.add_loaned_copy()
	# book.add_loaned_copy()
	# book.add_loaned_copy()
	# print("\nAfter borrowing one copy:")
	# print(book)  # הדפסת מצב הספר לאחר השאלה
	#
	# # החזרת ספר
	# book.return_loaned_copy()
	# book.return_loaned_copy()
	# book.return_loaned_copy()
	# book.return_loaned_copy()
	# print("\nAfter returning one copy:")
	# print(book)  # הדפסת מצב הספר לאחר החזרה
	# יצירת DataFrame לדוגמה

	# יצירת מחלקת חיפוש (למשל, חיפוש לפי שם)
	search_manager = SearchManager(SearchByName())
	results = search_manager.search(books, "Python")
	print("Books found by name:")
	print(results)

	# יצירת איטרטור לספרים שנמצאו
	iterator = BookIterator(results)

	print("\nIterating through found books:")
	for book in iterator:
		print(book)

if __name__ == "__main__":
	main()


