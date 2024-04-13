import mysql.connector

def create_database():
    connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sharon1597536987410')
    mycursor = connection.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS WellRead")
    connection.close()

create_database()

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sharon1597536987410',
        database="WellRead")


def create_Book_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE  IF NOT EXISTS Books (
        BookId INT AUTO_INCREMENT PRIMARY KEY,
        Title VARCHAR(255) NOT NULL,
        Author VARCHAR(255),
        Genre VARCHAR(100),
        year int,
        ShelfLocation VARCHAR(255),
        Status ENUM('available', 'unavailable') )
    """)
    print("Books Table created")


def create_Members_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE  IF NOT EXISTS Members (
        MembersId INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(12),
        MembershipType ENUM('gold', 'regular') NOT NULL,
        MembershipStartDate DATE)
    """)
    print("Members Table created")

def create_Loan_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE  IF NOT EXISTS Loan (
        LoanId INT AUTO_INCREMENT PRIMARY KEY,
        BookId INT,
        MembersId INT,
        LoanDate DATE,
        DueDate DATE,
        ReturnDate DATE,
        Status ENUM('open', 'close' , 'delay') NOT NULL,
        CONSTRAINT fk_book FOREIGN KEY (BookId) REFERENCES Books(BookId),
        CONSTRAINT fk_member FOREIGN KEY (MembersId) REFERENCES Members(MembersId))
    """)
    print("Loan Table created")

def create_Fine_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE  IF NOT EXISTS Fine (
        FineId INT AUTO_INCREMENT PRIMARY KEY,
        LoanId INT,
        Amount INT,
        Status ENUM ('paid' , 'not paid') NOT NULL,
        CONSTRAINT fk_loan FOREIGN KEY (LoanId) REFERENCES Loan(LoanId)
    )
    """)
    print("Fine Table created")

def create_Employee_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE  IF NOT EXISTS Employee (
        EmployeeId INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(12),
        EmployeeType ENUM ('Manager' , 'Employee' ),
        Password VARCHAR(100)
        )
    """)

    print("Employee Table created")

def create_WaitingList_table():
    connection = connect_to_db()
    mycursor = connection.cursor()
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS WaitingList (
    BookID INT,
    MemberID INT,
    Book_Title VARCHAR(255),
    OrderNumber INT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (BookID, MemberID),
    FOREIGN KEY (BookID) REFERENCES Books(BookId),
    FOREIGN KEY (MemberID) REFERENCES Members(MembersId)
);
    )""", multi=True)
    print("WaitingList Table created")

create_database()
create_Book_table()
create_Loan_table()
create_Fine_table()
create_Employee_table()
create_Members_table()
create_WaitingList_table()
