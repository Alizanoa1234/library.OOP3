from data.dataManager import DataManager
from data.books import load_books_to_dataframe


def main():
    # Load the data from the CSV file
    file_path = "books.csv"
    load_books_to_dataframe(file_path)  # Initialize DataManager with the loaded data

    # Get the DataFrame from DataManager
    data_manager = DataManager.get_instance()
    data_frame = data_manager.get_data()
    if data_frame is not None:
        print("Loaded DataFrame:")
        print(data_frame)
    else:
        print("DataFrame is empty or not initialized.")

    # # 3. Create a Book object from a DataFrame row
	# row = data_frame.iloc[0]  # First row of the DataFrame
	# book = Book(
	# 	title=row["title"],
	# 	author=row["author"],
	# 	category=row["genre"],
	# 	year=int(row["year"]),
	# 	copies=int(row["copies"]),
	# 	is_loaned_status=row["is_loaned"]
	# )
	# print("\nBook object created from the first row:")
	# print(book)
	#
	# # 4. Update the book object
	# book.add_loaned_copy("user123")
	# print("\nBook object after loaning a copy:")
	# print(book)
	#
	# # 5. Update the DataFrame based on the book object
	# update_book_in_dataframe(book)
	# print("\nDataFrame after updating the book:")
	# print(data_frame)
	#
	# # 6. Save the updated DataFrame to a CSV file
	# save_updated_dataframe("updated_books.csv")
	# print("\nData saved to updated_books.csv")
	#

	# file_path = "books.csv"
	# books = load_books_to_dataframe(file_path)
	#
	# # Set Pandas display options to avoid truncation of data
	# pd.set_option('display.max_columns', None)  # Show all columns
	# pd.set_option('display.max_colwidth', None)  # Do not truncate column content
	# pd.set_option('display.width', 1000)  # Set the display width to avoid line breaks
	# pd.set_option('display.max_rows', 10)  # Display only 10 rows at a time (can be adjusted)
	#
	# # Print the first 10 rows in full
	# print(books)

	#
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
	# book.return_loaned_copy()  # Return the first copy
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


	# Creating a search manager with a strategy (e.g., search by name)
	# search_manager = SearchManager(SearchByName())
	#
	# # Searching for books by the name "Python"
	# results = search_manager.search(books, "Python")
	# print("Books found by name:")
	# print(results)
	#
	# # Creating an iterator for the found books
	# iterator = BookIterator(results)

	# print("\nIterating through found books:")
	# for book in iterator:
	# 	print(book)

if __name__ == "__main__":
	main()


