import tkinter as tk
from tkinter import messagebox, ttk
from Employee import DatabaseManager, Employee


class EmployeeDialog(tk.Toplevel):
    def __init__(self, parent, title="Employee Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"Name": "", "Email": "", "Phone": "", "EmployeeType": "", "Password": ""}

        self.result = None

        # Setup fields
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, initial_values["Name"])

        tk.Label(self, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.insert(0, initial_values["Email"])

        tk.Label(self, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.insert(0, initial_values["Phone"])

        tk.Label(self, text="Employee Type:").grid(row=3, column=0, padx=5, pady=5)
        self.employee_type_var = tk.StringVar(self)
        self.employee_type_var.set(initial_values["EmployeeType"])  # Set default value
        self.employee_type_entry = ttk.Combobox(self, textvariable=self.employee_type_var, values=["Manager", "Employee"])
        self.employee_type_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Password:").grid(row=4, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=1, padx=5, pady=5)
        self.password_entry.insert(0, initial_values["Password"])

        # Setup buttons
        tk.Button(self, text="OK", command=self.on_ok).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=5, column=1, padx=5, pady=5)

        self.grab_set()  # Make window modal
        self.wait_visibility()
        self.focus_set()

    def on_ok(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        employee_type = self.employee_type_var.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not phone or not employee_type or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.result = {"Name": name, "Email": email, "Phone": phone, "EmployeeType": employee_type, "Password": password}
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result


class EmployeeManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Employee Management System")

        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview setup
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone", "EmployeeType", "Password"), show="headings")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("EmployeeType", text="Employee Type")
        self.tree.heading("Password", text="Password")

        # Buttons Frame for responsiveness
        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        window.grid_columnconfigure(0, weight=1)

        # Button labels and corresponding actions
        button_labels = ['Add', 'Update', 'Delete', 'Refresh']
        actions = [self.add_employee, self.update_employee, self.delete_employee, self.refresh_employee_list]

        # Create buttons with text labels and assign commands
        for i, (label, action) in enumerate(zip(button_labels, actions)):
            ttk.Button(btn_frame, text=label, command=action).grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)

        self.refresh_employee_list()

    def refresh_employee_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for employee in DatabaseManager.get_employees():
            self.tree.insert('', 'end', values=(employee.id, employee.name, employee.email, employee.phone, employee.employee_type, employee.password))

    def add_employee(self):
        dialog = EmployeeDialog(self.window, "Add Employee")
        result = dialog.show()
        if result:  # Check if result is not None
            employee = Employee(result["Name"], result["Email"], result["Phone"], result["EmployeeType"], result["Password"])
            DatabaseManager.add_employee(employee)
            self.refresh_employee_list()

    def update_employee(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"Name": item[1], "Email": item[2], "Phone": item[3], "EmployeeType": item[4], "Password": item[5]}
            dialog = EmployeeDialog(self.window, "Update Employee", initial_values)
            result = dialog.show()
            if result:  # Check if result is not None
                employee = Employee(result["Name"], result["Email"], result["Phone"], result["EmployeeType"], result["Password"], item[0])
                DatabaseManager.update_employee(employee)
                self.refresh_employee_list()
        else:
            messagebox.showwarning("Warning", "Please select an employee to update.")

    def delete_employee(self):
        selected = self.tree.selection()
        if selected:
            employee_id = self.tree.item(selected[0], 'values')[0]
            DatabaseManager.delete_employee(employee_id)
            self.refresh_employee_list()
        else:
            messagebox.showwarning("Warning", "Please select an employee to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementGUI(root)
    root.mainloop()
