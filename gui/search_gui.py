from services.library_manager import LibraryManager

library_manager = LibraryManager("data/books.csv", [])

def search_books():
    """
    Displays the search menu for books.
    """
    while True:
        print("""
--- Search Books ---
1. Search by Title
2. Search by Author
3. Search by Category
4. Search by Year
5. Back to Main Menu

""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            query = input("Enter book title: ").strip()
            results = library_manager.search_books(query, search_by="title")
            display_results(results)
        elif choice == "2":
            query = input("Enter author: ").strip()
            results = library_manager.search_books(query, search_by="author")
            display_results(results)
        elif choice == "3":
            query = input("Enter category: ").strip()
            results = library_manager.search_books(query, search_by="category")
            display_results(results)
        elif choice == "4":
            query = input("Enter year: ").strip()
            results = library_manager.search_books(query, search_by="year")
            display_results(results)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def display_results(results):
    """
    Displays the search results.
    """
    if results:
        print("\nSearch Results:")
        for book in results:
            print(f"{book.title} by {book.author} ({book.year}) - {book.available} copies available.")
    else:
        print("No books found.")
