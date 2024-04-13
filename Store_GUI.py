import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Employee import DatabaseManager, Employee
from Book_GUI import BookManagementGUI
from Loan_GUI import LoanManagementGUI
from Member_GUI import MemberManagementGUI

class LoginGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Login")

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Initialize GUI components
        self.init_gui()

    def init_gui(self):
        ttk.Label(self.frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_entry = ttk.Entry(self.frame)  # Using id_entry
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)  # Adjusted to id_entry

        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2, padx=5, pady=5)

    def login(self):
        id = self.id_entry.get()  # Using id_entry to get the employee ID
        password = self.password_entry.get()

        # Check if the username and password match an employee in the database
        employee = DatabaseManager.authenticate(id, password)
        if employee:
            # Open the main application window with the authenticated employee
            self.parent.destroy()
            root = tk.Tk()
            app = StoreGUI(root, employee)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class StoreGUI:
    def __init__(self, parent, employee):
        self.parent = parent
        self.parent.title(f"Employee Panel - {employee.name}")

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.employee = employee

        # Initialize GUI components
        self.init_gui()

    def init_gui(self):
        # Display employee information
        ttk.Label(self.frame, text=f"Welcome, {self.employee.name}").grid(row=0, columnspan=2, padx=5, pady=5)

        # Button for book management
        ttk.Button(self.frame, text="Book Management", command=self.open_book_management).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Button for loan management
        ttk.Button(self.frame, text="Loan Management", command=self.open_loan_management).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Button for members management
        ttk.Button(self.frame, text="Members Management", command=self.open_members_management).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        print("Employee Type:", self.employee.employee_type)
        # Only display employee management button for manager
        if self.employee.employee_type == 'Manager':
            ttk.Button(self.frame, text="Employee Management", command=self.open_employee_management).grid(row=4,
                                                                                                           column=0,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="ew")



    def open_book_management(self):
        # Open Book Management window
        book_root = tk.Toplevel(self.parent)
        book_app = BookManagementGUI(book_root)

    def open_loan_management(self):
        # Open Loan Management window
        loan_root = tk.Toplevel(self.parent)
        loan_app = LoanManagementGUI(loan_root)

    def open_members_management(self):
        # Open Members Management window
        members_root = tk.Toplevel(self.parent)
        members_app = MemberManagementGUI(members_root)

    def open_employee_management(self):
        # Implement employee management functionality
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()
