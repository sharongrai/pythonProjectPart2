import mysql.connector
from datetime import datetime, timedelta


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

class ReportPrinter:
    def __init__(self, name, date, id=None):
        self.id = id
        self.name = name
        self.date = date


# ************ - report printer management functions - ************
class DatabaseManager:
    @staticmethod
    def generate_report(report_type, option, start_date, end_date, month=None, year=None):
        if option == 1:  # Date range option selected
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        elif option == 2:  # Month option selected
            # Set start date to the first day of the selected month and end date to the last day
            start_date = datetime(int(year), int(month), 1)
            end_date = start_date.replace(day=1, month=start_date.month % 12 + 1) - timedelta(days=1)

        if report_type == "Loan Report":
            loan_records = DatabaseManager.get_loan_records_by_date_range(start_date, end_date)
            report = DatabaseManager.generate_loan_report(loan_records, start_date, end_date)
        elif report_type == "Return Report":
            return_records = DatabaseManager.get_return_records_by_date_range(start_date, end_date)
            report = DatabaseManager.generate_return_report(return_records, start_date, end_date)
        elif report_type == "Popular Books Report":
            loan_records = DatabaseManager.get_loan_records_by_date_range(start_date, end_date)
            report = DatabaseManager.generate_popular_books_report(loan_records)

        return report

    @staticmethod
    def get_loan_records_by_date_range(start_date, end_date):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM loan WHERE LoanDate BETWEEN %s AND %s", (start_date, end_date))
            return db.cursor.fetchall()

    @staticmethod
    def generate_loan_report(loan_records, start_date, end_date):
        report = []
        for loan in loan_records:
            if start_date <= loan.loanDate <= end_date:
                report.append((loan.id, loan.book_id, loan.member_id, loan.loanDate, loan.dueDate, loan.returnDate, loan.status))
        return report
