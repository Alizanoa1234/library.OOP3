import unittest

from data.books import load_books_from_file, DataManager


class TestDataManager(unittest.TestCase):
    def test_load_books(self):
        # בדוק אם הנתונים נטענו כראוי
        load_books_from_file("test_books.csv")
        data = DataManager.get_instance().get_data()
        self.assertFalse(data.empty)

    def test_update_book_in_dataframe(self):
        # צור ספר, עדכן, וודא שהתוצאה נכונה
        pass
if __name__ == '__main__':
	unittest.main()
