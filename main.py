# main.py

from data.books import load_books_from_file, save_books_to_file
from data.users import LibrarianManager


def main():
	# Load books from the CSV file
	books = load_books_from_file("books.csv")

	# Print the books info before any action (without modifying anything)
	print("Books available before any action:")
	for book in books:
		print(book)

	# Save the updated books list to the CSV file
#	save_books_to_file(books, "books.csv")

	# יצירת אובייקט של המחלקה
	manager = LibrarianManager()

	# בדיקה: יצירת קובץ
	print("=== Testing file creation ===")
	manager._initialize_users_file()

	# בדיקה: הוספת ספרן
	print("\n=== Testing user addition ===")
	success, message = manager.register_librarian("admin", "securepassword123")
	success, message = manager.register_librarian("admin2", "123")
	print(message)

	# בדיקה: קריאת הקובץ
	print("\n=== Testing file reading ===")
	with open(manager.USERS_FILE, 'r') as file:
		for row in file:
			print(row.strip())

if __name__ == "__main__":
	main()


from models.book import Book
