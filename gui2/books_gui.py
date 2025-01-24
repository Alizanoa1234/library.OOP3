import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from data.books import DataManager, load_books_from_file  # Import the existing DataManager class
from logs.actions import log_error, log_info
from models.search_strategy import SearchManager, SearchByName, SearchByAuthor, SearchByGenre, SearchByYear
from services.library_manager import LibraryManager


class BooksGUI:
    def __init__(self, root, csv_file):
        """
        Initialize the Books Management GUI.

        Args:
            root (tk.Tk): The Tkinter window for books management.
            csv_file (str): Path to the CSV file for the library.
        """
        self.root = root
        self.root.title("Books Management")
        self.csv_file = csv_file

        # Load books into DataManager
        load_books_from_file(self.csv_file)
        self.manager = DataManager.get_instance()

        # Load books from the CSV file
     #   self.load_books()

        # Configure the GUI layout
        self.configure_layout()

    def load_books(self):
        """
        Load books from the CSV file using the processing function.
        """
        try:
            # Load and process the file using the defined function
            load_books_from_file(self.csv_file)

            # Check if DataManager has valid data
            books_df = self.manager.get_data()
            if books_df is None or books_df.empty:
                raise ValueError("The books DataFrame is empty or invalid.")

            # DataManager is initialized within the function
            print("Books loaded and processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load and process books: {e}")

    def configure_layout(self):
        """
        Configure the layout of the Books Management GUI.
        """
        # Create the main treeview for displaying books
        self.tree = ttk.Treeview(self.root, columns=(
            "index", "title", "author", "genre", "year", "copies",
            "is_loaned", "available", "borrow_count", "popularity_score", "waiting_list"
        ), show="headings")

        # Set column headers and their widths
        self.tree.heading("index", text="Index")
        self.tree.column("index", width=50, anchor="center")  # Small column for index
        self.tree.heading("title", text="Title")
        self.tree.column("title", width=150)  # Title column width
        self.tree.heading("author", text="Author")
        self.tree.column("author", width=100)  # Author column width
        self.tree.heading("genre", text="Genre")
        self.tree.column("genre", width=100)  # Genre column width
        self.tree.heading("year", text="Year")
        self.tree.column("year", width=80, anchor="center")  # Year column width
        self.tree.heading("copies", text="Copies")
        self.tree.column("copies", width=80, anchor="center")  # Copies column width
        self.tree.heading("is_loaned", text="Is Loaned")
        self.tree.column("is_loaned", width=100, anchor="center")  # Is Loaned column width
        self.tree.heading("available", text="Available")
        self.tree.column("available", width=100, anchor="center")  # Available column width
        self.tree.heading("borrow_count", text="Borrow Count")
        self.tree.column("borrow_count", width=100, anchor="center")  # Borrow Count column width
        self.tree.heading("popularity_score", text="Popularity Score")
        self.tree.column("popularity_score", width=120, anchor="center")  # Popularity Score column width
        self.tree.heading("waiting_list", text="Waiting List")
        self.tree.column("waiting_list", width=200)  # Waiting List column width
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons for managing books
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        tk.Button(self.button_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Borrow Book", command=self.borrow_book).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Return Book", command=self.return_book).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Search Books", command=self.search_books).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Save to CSV", command=self.save_to_csv).pack(side=tk.LEFT, padx=5, pady=5)

        # Refresh the treeview with the current data
        self.refresh_tree()

    def refresh_tree(self):
        """
        Refresh the treeview with the processed data from DataManager.
        """
        # Clear the existing rows in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Retrieve the processed data from DataManager
        books_df = self.manager.get_data()

        # Insert each row into the treeview, including the new columns
        for idx, (_, row) in enumerate(books_df.iterrows(), start=1):
            self.tree.insert("", tk.END, values=(
                idx, row["title"], row["author"], row["genre"], row["year"],
                row["copies"], row["is_loaned"], row["available"],
                row["borrow_count"], row["popularity_score"], row["waiting_list"]
            ))

    def add_book(self):
        """
        Add a new book to the library.
        """

        def save_new_book():
            title = title_var.get()
            author = author_var.get()
            genre = genre_var.get()
            year = year_var.get()
            copies = copies_var.get()


            # בדיקת שדות
            if not (title and author and year and copies):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                # יצירת מילון עבור is_loaned
                is_loaned_dict = {i + 1: "no" for i in range(int(copies))}

                # אתחול יתר השדות בערכים מתאימים כברירת מחדל
                genre = "Uncategorized"  # קטגוריה כללית כברירת מחדל
                waiting_list = "[]"  # רשימת המתנה ריקה
                borrow_count = 0  # הספר עדיין לא הושאל
                popularity_score = 0  # ניקוד פופולריות ראשוני

                # הוספת הספר החדש ל-DataFrame
                new_row = pd.DataFrame([{
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "year": int(year),
                    "copies": int(copies),
                    "is_loaned": str(is_loaned_dict),  # מילון המייצג את מצב ההשאלה
                    "available": int(copies),  # כל העותקים זמינים בהתחלה
                    "borrow_count": borrow_count,  # הספר עדיין לא הושאל
                    "popularity_score": popularity_score,  # ניקוד פופולריות ראשוני
                    "waiting_list": waiting_list  # רשימת המתנה ריקה
                }])

                books_df = self.manager.get_data()
                books_df = pd.concat([books_df, new_row], ignore_index=True)
                self.manager.initialize_data(books_df)
                self.refresh_tree()
                add_window.destroy()
                messagebox.showinfo("Success", "Book added successfully!")
                log_info(f"Book '{title}' added successfully.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")
                log_error(f"Failed to add book '{title}'. Error: {e}")

        # חלון להוספת ספר חדש
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")

        tk.Label(add_window, text="Title").pack()
        title_var = tk.StringVar()
        tk.Entry(add_window, textvariable=title_var).pack()

        tk.Label(add_window, text="Author").pack()
        author_var = tk.StringVar()
        tk.Entry(add_window, textvariable=author_var).pack()

        tk.Label(add_window, text="genre").pack()
        genre_var = tk.StringVar()
        tk.Entry(add_window, textvariable=genre_var).pack()

        tk.Label(add_window, text="Year").pack()
        year_var = tk.StringVar()
        tk.Entry(add_window, textvariable=year_var).pack()

        tk.Label(add_window, text="Copies").pack()
        copies_var = tk.StringVar()
        tk.Entry(add_window, textvariable=copies_var).pack()

        tk.Button(add_window, text="Save", command=save_new_book).pack()

    def borrow_book(self):
        """
        Borrow a book from the library using LibraryManager logic and user details.
        """
        # Check if a book is selected in the TreeView
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            log_error("Borrow book failed: No book selected by the user.")
            return

        # Retrieve the selected book's title and author
        book_title = self.tree.item(selected_item, "values")[1]
        book_author = self.tree.item(selected_item, "values")[2]

        # Create a user details input window
        user_window = tk.Toplevel(self.root)
        user_window.title("User Details for Borrowing")

        tk.Label(user_window, text="Enter your name:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(user_window, textvariable=name_var).pack(pady=5)

        tk.Label(user_window, text="Enter your phone number:").pack(pady=5)
        phone_var = tk.StringVar()
        tk.Entry(user_window, textvariable=phone_var).pack(pady=5)

        tk.Label(user_window, text="Enter your email:").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(user_window, textvariable=email_var).pack(pady=5)

        def validate_and_borrow():
            """
            Validate user input and complete the borrowing process.
            """
            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()

            # Validate input fields
            if not name or not phone or not email:
                messagebox.showerror("Error", "All fields are required!")
                return

            if not phone.isdigit() or len(phone) < 9:
                messagebox.showerror("Error",
                                     "Invalid phone number. Must contain only digits and be at least 9 characters long.")
                return

            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Invalid email address format.")
                return

            # Proceed with borrowing logic if all inputs are valid
            try:
                books_df = self.manager.get_data()
                book_row = books_df[(books_df["title"] == book_title) & (books_df["author"] == book_author)]
                if book_row.empty:
                    messagebox.showerror("Error", f"Book '{book_title}' by {book_author} not found in the library.")
                    log_error(f"Borrow book failed: Book '{book_title}' not found.")
                    return

                row_index = book_row.index[0]

                # Check if there are available copies
                if books_df.at[row_index, "available"] <= 0:
                    messagebox.showinfo("Waiting List",
                                        f"No copies available for '{book_title}'. You have been added to the waiting list.")
                    waiting_list = eval(books_df.at[row_index, "waiting_list"])
                    waiting_list.append({"name": name, "phone": phone, "email": email})
                    books_df.at[row_index, "waiting_list"] = str(waiting_list)
                    self.manager.initialize_data(books_df)
                    self.refresh_tree()
                    log_info(f"User '{name}' added to waiting list for book '{book_title}'.")
                    user_window.destroy()
                    return

                # Update available copies and borrow the book
                is_loaned_dict = eval(books_df.at[row_index, "is_loaned"])
                for copy_id, status in is_loaned_dict.items():
                    if status == "no":
                        is_loaned_dict[copy_id] = "yes"
                        books_df.at[row_index, "is_loaned"] = str(is_loaned_dict)
                        books_df.at[row_index, "available"] -= 1
                        books_df.at[row_index, "borrow_count"] += 1
                        books_df.at[row_index, "popularity_score"] += 1
                        self.manager.initialize_data(books_df)
                        self.refresh_tree()
                        messagebox.showinfo("Success",
                                            f"Book '{book_title}' (Copy ID: {copy_id}) borrowed successfully!")
                        log_info(
                            f"Book '{book_title}' (Copy ID: {copy_id}) borrowed by user '{name}', phone: {phone}, email: {email}.")
                        user_window.destroy()
                        return

            except Exception as e:
                log_error(f"Borrow book failed for '{book_title}'. Error: {e}")
                messagebox.showerror("Error", f"Failed to borrow book: {e}")

        # Add buttons for validation and cancel
        tk.Button(user_window, text="Borrow", command=validate_and_borrow).pack(pady=10)
        tk.Button(user_window, text="Cancel", command=user_window.destroy).pack(pady=5)

    def return_book(self):
        """
        Return a borrowed book to the library.
        """
        # בדיקה אם נבחר ספר בטבלה
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            log_error("Return book failed: No book selected by the user.")
            return

        # שליפת פרטי הספר שנבחר
        book_title = self.tree.item(selected_item, "values")[1]  # כותרת הספר
        book_author = self.tree.item(selected_item, "values")[2]  # מחבר הספר

        try:
            # קבלת נתוני הספרים
            books_df = self.manager.get_data()
            book_row = books_df[(books_df["title"] == book_title) & (books_df["author"] == book_author)]
            if book_row.empty:
                messagebox.showerror("Error", f"Book '{book_title}' by {book_author} not found.")
                log_error(f"Return book failed: Book '{book_title}' not found.")
                return

            row_index = book_row.index[0]

            # טיפול בעמודת is_loaned (נניח שהיא כבר במבנה מילון)
            is_loaned_dict = books_df.at[row_index, "is_loaned"]  # הערך כבר במבנה מילון
            if isinstance(is_loaned_dict, str):
                is_loaned_dict = eval(is_loaned_dict)  # במקרה של מחרוזת, נבצע eval (בדיקת ביטחון בלבד)

            for copy_id, status in is_loaned_dict.items():
                if status == "yes":  # מציאת עותק מושאל
                    is_loaned_dict[copy_id] = "no"  # סימון העותק כפנוי
                    books_df.at[row_index, "is_loaned"] = is_loaned_dict

                    # עדכון עותקים זמינים
                    books_df.at[row_index, "available"] += 1

                    # טיפול ברשימת המתנה (אם קיימת)
                    waiting_list = books_df.at[row_index, "waiting_list"]
                    if isinstance(waiting_list, str):
                        waiting_list = eval(waiting_list)  # במקרה של מחרוזת, נבצע eval

                    if waiting_list:
                        next_user = waiting_list.pop(0)
                        books_df.at[row_index, "waiting_list"] = waiting_list
                        messagebox.showinfo("Waiting List",
                                            f"The book is now available for the next user in the waiting list: {next_user}.")
                        log_info(f"User {next_user} notified for book '{book_title}'.")

                    # שמירת הנתונים ועדכון תצוגה
                    self.manager.initialize_data(books_df)
                    self.refresh_tree()
                    messagebox.showinfo("Success", f"Book '{book_title}' (Copy ID: {copy_id}) returned successfully!")
                    log_info(f"Book '{book_title}' returned successfully. Copy ID: {copy_id}.")
                    return

            # אם אין עותקים מושאלים
            messagebox.showerror("Error", f"All copies of '{book_title}' are already available.")
            log_error(f"Return book failed: All copies of '{book_title}' are already available.")

        except Exception as e:
            log_error(f"Return book failed for '{book_title}'. Error: {e}")
            messagebox.showerror("Error", f"Failed to return book: {e}")

    def search_books(self):
        """
        Open a search window to find books based on user input.
        """
        # יצירת חלון חיפוש חדש
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Books")

        # שדה להזנת שאילתת חיפוש
        tk.Label(search_window, text="Enter search query:").pack(pady=5)
        query_var = tk.StringVar()
        tk.Entry(search_window, textvariable=query_var).pack(pady=5)

        # Dropdown לבחירת סוג החיפוש
        search_type_var = tk.StringVar(value="name")  # ברירת מחדל: חיפוש לפי שם
        tk.Label(search_window, text="Select search type:").pack(pady=5)
        search_type_dropdown = ttk.Combobox(search_window, textvariable=search_type_var)
        search_type_dropdown['values'] = ["name", "author", "genre", "year"]
        search_type_dropdown.pack(pady=5)

        # טבלה להצגת תוצאות החיפוש
        results_tree = ttk.Treeview(search_window, columns=(
            "index", "title", "author", "genre", "year", "copies",
            "is_loaned", "available", "borrow_count", "popularity_score"
        ), show="headings")
        results_tree.heading("index", text="Index")
        results_tree.heading("title", text="Title")
        results_tree.heading("author", text="Author")
        results_tree.heading("genre", text="Genre")
        results_tree.heading("year", text="Year")
        results_tree.heading("copies", text="Copies")
        results_tree.heading("is_loaned", text="Is Loaned")
        results_tree.heading("available", text="Available")
        results_tree.heading("borrow_count", text="Borrow Count")
        results_tree.heading("popularity_score", text="Popularity Score")
        results_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        def perform_search():
            """
            Perform the search based on user input and update the results treeview.
            """
            query = query_var.get().strip()
            search_type = search_type_var.get()

            # בדיקה אם השאילתא ריקה
            if not query:
                messagebox.showerror("Error", "Search query cannot be empty!")
                return

            # קביעת האסטרטגיה לפי סוג החיפוש שנבחר
            if search_type == "name":
                strategy = SearchByName()
            elif search_type == "author":
                strategy = SearchByAuthor()
            elif search_type == "genre":
                strategy = SearchByGenre()
            elif search_type == "year":
                strategy = SearchByYear()
            else:
                messagebox.showerror("Error", f"Invalid search type: {search_type}")
                return

            try:
                # ביצוע החיפוש באמצעות SearchManager
                search_manager = SearchManager(strategy)
                books_df = self.manager.get_data()  # קבלת נתוני הספרים
                results = search_manager.search(books_df, query)

                # ניהול תוצאות
                for row in results_tree.get_children():
                    results_tree.delete(row)

                for idx, (_, row) in enumerate(results.iterrows(), start=1):
                    results_tree.insert("", tk.END, values=(
                        idx, row["title"], row["author"], row["genre"], row["year"],
                        row["copies"], row["is_loaned"], row["available"],
                        row["borrow_count"], row["popularity_score"]
                    ))

                # לוגים בהתאם לתוצאות
                if not results.empty:
                    log_info(f"Search '{search_type}' succeeded for query '{query}'. {len(results)} results found.")
                else:
                    log_info(f"Search '{search_type}' completed for query '{query}', but no results found.")

            except Exception as e:
                log_error(f"Search '{search_type}' failed for query '{query}'. Error: {e}")
                messagebox.showerror("Error", f"An error occurred during the search: {e}")

        # כפתורים לביצוע חיפוש ולסגירת החלון
        tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        tk.Button(search_window, text="Close", command=search_window.destroy).pack(pady=5)

    def save_to_csv(self):
        """
        Save the current data to the CSV file.
        """
        try:
            books_df = self.manager.get_data()
            books_df.to_csv(self.csv_file, index=False)
            messagebox.showinfo("Success", "Library data saved to CSV successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = BooksGUI(root, "C:/Users/sapir/PycharmProjects/library.OOP3/data/books.csv")
    root.mainloop()