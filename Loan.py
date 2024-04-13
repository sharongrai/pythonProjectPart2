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

class Loan:
    def __init__(self, bookID, membersID, loanDate, dueDate, returnDate=None, status='open', id=None):
        self.id = id
        self.bookID = bookID
        self.membersID = membersID
        self.loanDate = loanDate
        self.dueDate = dueDate
        self.returnDate = returnDate
        self.status = status

class DatabaseManager:
    @staticmethod
    def add_loan(loan):
        if isinstance(loan, Loan):
            with DatabaseConnection() as db:
                db.cursor.execute("INSERT INTO loan (BookID, MembersID, LoanDate, DueDate, ReturnDate, Status) VALUES (%s, %s, %s, %s, %s, %s)",
                                  (loan.bookID, loan.membersID, loan.loanDate, loan.dueDate, loan.returnDate, loan.status))

    @staticmethod
    def update_loan(loan):
        if isinstance(loan, Loan):
            with DatabaseConnection() as db:
                db.cursor.execute("UPDATE loan SET ReturnDate = %s, Status = %s WHERE LoanID = %s",
                                  (loan.returnDate, loan.status, loan.id))

    @staticmethod
    def get_loan():
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT LoanID, BookID, MembersID, LoanDate, DueDate, ReturnDate, Status FROM loan")
            loans = db.cursor.fetchall()
            return [Loan(id=id, bookID=bookID, membersID=membersID, loanDate=loanDate, dueDate=dueDate, returnDate=returnDate, status=status)
                    for id, bookID, membersID, loanDate, dueDate, returnDate, status in loans]

    @staticmethod
    def search_loan(query):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT loanID, bookID, MembersID, loanDate, dueDate, returnDate, status FROM loan WHERE bookID LIKE %s OR MembersID LIKE %s OR loanDate LIKE %s OR dueDate LIKE %s OR returnDate LIKE %s OR status LIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            loans = db.cursor.fetchall()
            return [Loan(id=id, bookID=bookID, membersID=MembersID, loanDate=loanDate, dueDate=dueDate,
                         returnDate=returnDate, status=status)
                    for id, bookID, MembersID, loanDate, dueDate, returnDate, status in loans]
