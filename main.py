# main.py

from data.books import load_books_from_file, save_books_to_file
def main():
	# Load books from the CSV file
	books = load_books_from_file("books.csv")

	# Print the books info before any action (without modifying anything)
	print("Books available before any action:")
	for book in books:
		print(book)

	# Save the updated books list to the CSV file
#	save_books_to_file(books, "books.csv")


if __name__ == "__main__":
	main()


from models.book import Book
