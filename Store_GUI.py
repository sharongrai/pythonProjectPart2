import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Employee import DatabaseManager, Employee
from Book_GUI import BookManagementGUI
from Employee_GUI import EmployeeManagementGUI
from Loan_GUI import LoanManagementGUI
from Member_GUI import MemberManagementGUI

#log in window
from ReportPrinter_GUI import ReportPrinterGUI


class LoginGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Login")

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.init_gui()

    def init_gui(self):
        ttk.Label(self.frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_entry = ttk.Entry(self.frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2, padx=5, pady=5)

    def login(self):
        id = self.id_entry.get()
        password = self.password_entry.get()

        #check if the username and password matches an employee in the database
        employee = DatabaseManager.authenticate(id, password)
        if employee:
            self.parent.destroy()
            root = tk.Tk()
            app = StoreGUI(root, employee)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

#options window
class StoreGUI:
    def __init__(self, parent, employee):
        self.parent = parent
        self.parent.title(f"Employee Panel - {employee.name}")

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.employee = employee

        self.init_gui()

    def init_gui(self):
        ttk.Label(self.frame, text=f"Welcome, {self.employee.name}").grid(row=0, columnspan=2, padx=5, pady=5)

        #Book Management window
        ttk.Button(self.frame, text="Book Management", command=self.open_book_management).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        #Loan Management window
        ttk.Button(self.frame, text="Loan Management", command=self.open_loan_management).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        #Members Management window
        ttk.Button(self.frame, text="Members Management", command=self.open_members_management).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        print("Employee Type:", self.employee.employee_type)

        #Generate Reports window
        ttk.Button(self.frame, text="Generate Reports", command=self.open_report_management).grid(row=4, column=0,padx=5, pady=5,sticky="ew")

        #only display employee management button for manager
        if self.employee.employee_type == 'Manager':
            ttk.Button(self.frame, text="Employee Management", command=self.open_employee_management).grid(row=5,column=0,padx=5,pady=5,sticky="ew")


    def open_book_management(self):
        book_root = tk.Toplevel(self.parent)
        book_app = BookManagementGUI(book_root)

    def open_loan_management(self):
        loan_root = tk.Toplevel(self.parent)
        loan_app = LoanManagementGUI(loan_root)

    def open_members_management(self):
        members_root = tk.Toplevel(self.parent)
        members_app = MemberManagementGUI(members_root)

    def open_report_management(self):
        reports_root = tk.Toplevel(self.parent)
        members_app = ReportPrinterGUI(reports_root)

    def open_employee_management(self):
        employee_root = tk.Toplevel(self.parent)
        employee_app = EmployeeManagementGUI(employee_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()
