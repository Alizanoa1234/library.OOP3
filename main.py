import pandas as pd


from data.books import load_books_from_file, save_books_to_file, update_book_in_dataframe
from models.book import Book
from data.books import DataManager

def main():
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 0)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    # Step 1: Load books into DataManager
    file_path = "books.csv"
    print("=== Step 1: Loading Books ===")
    load_books_from_file(file_path)

    # Step 2: Get the DataFrame and display its contents
    data_manager = DataManager.get_instance()
    books_df = data_manager.get_data()

    if books_df is not None and not books_df.empty:
        print("\nLoaded DataFrame:")
        print(books_df)

    save_books_to_file(file_path)

    #
    #     # Step 3: Select a book to update
    #     print("\n=== Step 3: Updating a Book ===")
    #     # Simulate a book update
    #     sample_row = books_df.iloc[0]  # Get the first book in the DataFrame
    #     book_to_update = Book(
    #         title=sample_row['title'],
    #         author=sample_row['author'],
    #         year=int(sample_row['year']),
    #         category=sample_row['genre'],
    #         copies=int(sample_row['copies'])
    #     )
    #     book_to_update.is_loaned = sample_row['is_loaned']
    #     book_to_update.waiting_list = sample_row['waiting_list']
    #
    #     # Simulate changes
    #     book_to_update.copies += 1  # Add one copy
    #     book_to_update.is_loaned[book_to_update.copies] = 'no'  # New copy is available
    #     book_to_update.waiting_list.append("User123")  # Add a user to the waiting list
    #
    #     # Update the DataFrame
    #     update_book_in_dataframe(book_to_update)
    #
    #     # Display the updated DataFrame
    #     print("\nUpdated DataFrame:")
    #     print(books_df)
    #
    #     # Step 4: Save changes to file
    #     print("\n=== Step 4: Saving Changes ===")
    #     save_books_to_file(file_path)
    #
    # else:
    #     print("DataFrame is empty or not initialized.")

if __name__ == "__main__":
    main()
