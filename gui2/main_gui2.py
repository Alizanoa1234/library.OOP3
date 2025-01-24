import tkinter as tk
from user_gui import UserGUI
from gui2.books_gui import BooksGUI

if __name__ == "__main__":
    def on_login_success():
        """
        Callback function to open the main system after successful login.
        """
        print("Login successful! Opening main system...")

        # פתיחת המערכת הראשית
        main_window = tk.Toplevel()  # יצירת חלון חדש
        BooksGUI(main_window, "C:/Users/sapir/PycharmProjects/library.OOP3/data/books.csv")  # הפעלת GUI של הספרים
        main_window.mainloop()

    root = tk.Tk()
    app = UserGUI(root, on_login_success)
    root.mainloop()




