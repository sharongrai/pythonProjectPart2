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

class Employee:
    def __init__(self, name, email, phone, employee_type, password, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.employee_type = employee_type
        self.password = password

class DatabaseManager:
    @staticmethod
    def add_employee(employee):
        if isinstance(employee, Employee):
            with DatabaseConnection() as db:
                db.cursor.execute("INSERT INTO employee (Name, Email, Phone, EmployeeType, Password) VALUES (%s, %s, %s, %s, %s)",
                                  (employee.name, employee.email, employee.phone, employee.employee_type, employee.password))

    @staticmethod
    def update_employee(employee):
        if isinstance(employee, Employee):
            with DatabaseConnection() as db:
                db.cursor.execute("UPDATE employee SET Name = %s, Email = %s, Phone = %s, EmployeeType = %s, Password = %s WHERE EmployeeID = %s",
                                  (employee.name, employee.email, employee.phone, employee.employee_type, employee.password, employee.id))

    @staticmethod
    def get_employees():
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT EmployeeID, Name, Email, Phone, EmployeeType, Password FROM employee")
            employees = db.cursor.fetchall()
            return [Employee(id=id, name=name, email=email, phone=phone, employee_type=employee_type, password=password)
                    for id, name, email, phone, employee_type, password in employees]

    @staticmethod
    def search_employee(query):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, EmployeeType, Password FROM employee WHERE Name LIKE %s OR Email LIKE %s OR Phone LIKE %s OR EmployeeType LIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            employees = db.cursor.fetchall()
            return [Employee(id=id, name=name, email=email, phone=phone, employee_type=employee_type, password=password)
                    for id, name, email, phone, employee_type, password in employees]

    @staticmethod
    def delete_employee(employee_id):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM employee WHERE EmployeeId = %s" , (employee_id,))

    @staticmethod
    def authenticate(id, password):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, EmployeeType, Password FROM employee WHERE EmployeeID = %s AND Password = %s",
                (id, password))
            employee_data = db.cursor.fetchone()
            if employee_data:
                # Assign retrieved data to variables
                employee_id, name, email, phone, employee_type, password = employee_data
                # Create and return Employee object
                return Employee(id=employee_id, name=name, email=email, phone=phone, employee_type=employee_type,
                                password=password)
            else:
                return None