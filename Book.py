from tkinter import messagebox

import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sharon1597536987410',
            database="WellRead"
        )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class Book:
    def __init__(self, title, author, genre, year, shelfLocation, status, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.shelfLocation = shelfLocation
        self.status = status

class WaitingListEntry:
    def __init__(self, book_id, title, member_id,date_added):
        self.book_id = book_id
        self.title = title
        self.member_id = member_id
        self.date_added = date_added


class DatabaseManager:

    @staticmethod
    def add_book(book):
        if isinstance(book, Book):
            with DatabaseConnection() as db:
                db.cursor.execute(
                    "INSERT INTO books (Title, Author, Genre, Status, Year, ShelfLocation) VALUES (%s, %s, %s, %s, %s, %s)",
                    (book.title, book.author, book.genre, book.status, book.year, book.shelfLocation))

    @staticmethod
    def update_book(book):
        if isinstance(book, Book):
            with DatabaseConnection() as db:
                db.cursor.execute("UPDATE books SET Title = %s, Author = %s, Genre = %s, Year = %s, ShelfLocation = %s, Status = %s WHERE BookId = %s",
                                  (book.title, book.author, book.genre, book.year, book.shelfLocation, book.status, book.id))

    @staticmethod
    def get_books():
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT BookId, Title, Author, Genre, Year, ShelfLocation, Status FROM books")
            books = db.cursor.fetchall()
            return [Book(id=id, title=title, author=author, genre=genre, year=year, shelfLocation=shelfLocation, status=status)
                    for id, title, author, genre, year, shelfLocation, status in books]

    @staticmethod
    def search_books(query):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT BookId, Title, Author, Genre, Year, ShelfLocation, Status FROM books WHERE Title LIKE %s OR Author LIKE %s OR Genre LIKE %s OR Year LIKE %s OR ShelfLocation LIKE %s OR Status LIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            books = db.cursor.fetchall()
            return [Book(id=id, title=title, author=author, genre=genre, year=year, shelfLocation=shelfLocation, status=status)
                    for id, title, author, genre, year, shelfLocation, status in books]

    @staticmethod
    def delete_book(BookID):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM books WHERE BookID = %s", (BookID,))

    @staticmethod
    def register_to_waiting_list(book_id, member_id):
        with DatabaseConnection() as db:
            try:
                db.cursor.execute("SELECT MAX(OrderNumber) FROM WaitingList WHERE BookID = %s", (book_id,))
                max_order_number = db.cursor.fetchone()[0]
                if max_order_number is None:
                    order_number = 1
                else:
                    order_number = max_order_number + 1

                db.cursor.execute("INSERT INTO WaitingList (BookID, MemberID, OrderNumber) VALUES (%s, %s, %s)",
                                  (book_id, member_id, order_number))

            except Exception as e:
                messagebox.showerror("Error", f"Failed to register for waiting list: {e}")


    #waiting list functions

    def add_to_waiting_list(self, book_id, title, member_id):
        with DatabaseConnection() as db:
            db.cursor.execute("INSERT INTO WaitingList (BookID, MemberID, Book_Title) VALUES (%s, %s, %s)",(book_id,member_id,title))

    def remove_from_waiting_list(self, book_id, member_id):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM WaitingList WHERE BookID = %s AND MemberID = %s", (book_id, member_id))

    def get_highest_order_number(self, book_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT MAX(OrderNumber) FROM WaitingList WHERE BookID = %s", (book_id,))

            result = db.cursor.fetchone()[0]
            return result if result is not None else 0

    def get_waiting_list(self):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM WaitingList")
            return db.cursor.fetchall()

    def get_waiting_list_for_book(self, book_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM WaitingList WHERE BookID = %s", (book_id,))
            return db.cursor.fetchall()