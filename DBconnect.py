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

#insert to tables
def insert_books():
    connection = connect_to_db()
    mycursor = connection.cursor()
    insert_queries = [
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (1, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'A1', 'Available', 1960);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (2, '1984', 'George Orwell', 'Dystopian Fiction', 'B2', 'Available', 1949);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (3, 'Pride and Prejudice', 'Jane Austen', 'Classic Literature', 'C3', 'Available', 1813);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (4, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic Literature', 'D4', 'Available', 1925);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (5, 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 'E5', 'Available', 1951);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (6, 'Harry Potter and the Sorcerer\\'s Stone', 'J.K. Rowling', 'Fantasy', 'F6', 'Available', 1997);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (7, 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'G7', 'Available', 1937);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (8, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'H8', 'Available', 1960);",
        "INSERT INTO Books (BookId, Title, Author, Genre, ShelfLocation, Status, year) VALUES (9, 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'I9', 'Available', 1954);"
    ]

    for query in insert_queries:
        mycursor.execute(query)

    connection.commit()
    mycursor.close()
    connection.close()

def insert_members():
    connection = connect_to_db()
    mycursor = connection.cursor()
    insert_queries = [
        "INSERT INTO Members (Name, Email, Phone, MembershipType, MembershipStartDate) VALUES ('John Doe', 'john@gmail.com', '1234567890', 'gold', '2024-03-01');",
        "INSERT INTO Members (Name, Email, Phone, MembershipType, MembershipStartDate) VALUES ('Jane Smith', 'jane@hotmail.com', '9876543210', 'regular', '2024-03-05');",
        "INSERT INTO Members (Name, Email, Phone, MembershipType, MembershipStartDate) VALUES ('Bob Johnson', 'bob@gmail.com', '1112223333', 'gold', '2024-03-10');",
        "INSERT INTO Members (Name, Email, Phone, MembershipType, MembershipStartDate) VALUES ('Luck David', 'lukeD@walla.com', '1122334455', 'regular', '2024-03-26');"
    ]
    for query in insert_queries:
        mycursor.execute(query)

    connection.commit()
    mycursor.close()
    connection.close()

def insert_employees():
    connection = connect_to_db()
    mycursor = connection.cursor()
    insert_queries = [
        "INSERT INTO Employee (Name, Email, Phone, EmployeeType, Password) VALUES ('John Smith', 'john.smith@gmail.com', '123456789', 'Manager', '111');",
        "INSERT INTO Employee (Name, Email, Phone, EmployeeType, Password) VALUES ('Jane Doe', 'jane.doe@walla.com', '987654321', 'Manager', '222');",
        "INSERT INTO Employee (Name, Email, Phone, EmployeeType, Password) VALUES ('Michael Johnson', 'michael.johnson@gmail.com', '5551234567', 'Employee', '333');",
        "INSERT INTO Employee (Name, Email, Phone, EmployeeType, Password) VALUES ('Emily Brown', 'emily.brown@hotmail.com', '5559876543', 'Employee', '444');",
        "INSERT INTO Employee (Name, Email, Phone, EmployeeType, Password) VALUES ('Daniel Lee', 'daniel.lee@gmail.com', '5557891234', 'Employee', '555');"
    ]
    for query in insert_queries:
        mycursor.execute(query)

    connection.commit()
    mycursor.close()
    connection.close()

def insert_loans():
    connection = connect_to_db()
    mycursor = connection.cursor()
    insert_queries = [
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (1, 1, '2024-03-28', '2024-04-04', '2024-03-31', 'close');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (2, 2, '2024-03-29', '2024-04-05', NULL, 'open');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (3, 3, '2024-03-30', '2024-04-06', NULL, 'open');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (6, 1, '2024-03-31', '2024-04-07', NULL, 'open');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (8, 2, '2024-04-01', '2024-04-08', NULL, 'open');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (1, 1, '2024-03-30', '2024-05-30', NULL, 'open');",
        "INSERT INTO Loan (BookId, MembersId, LoanDate, DueDate, ReturnDate, Status) VALUES (7, 4, '2024-02-28', '2024-03-28', NULL, 'delay');"
    ]
    for query in insert_queries:
        mycursor.execute(query)

    connection.commit()
    mycursor.close()
    connection.close()