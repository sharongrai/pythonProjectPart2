import tkinter as tk
from tkinter import messagebox, ttk
from Loan import DatabaseManager, Loan

#add loan window
class LoanDialog(tk.Toplevel):
    def __init__(self, parent, title="Loan Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"bookID": "", "membersID": "", "loanDate": "", "dueDate": "", "returnDate": "", "status": ""}

        self.result = None

        # add loan fields
        tk.Label(self, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.book_id_entry.insert(0, initial_values["bookID"])

        tk.Label(self, text="Members ID:").grid(row=1, column=0, padx=5, pady=5)
        self.members_id_entry = tk.Entry(self)
        self.members_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.members_id_entry.insert(0, initial_values["membersID"])

        tk.Label(self, text="Loan Date:").grid(row=2, column=0, padx=5, pady=5)
        self.loan_date_entry = tk.Entry(self)
        self.loan_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.loan_date_entry.insert(0, initial_values["loanDate"])

        tk.Label(self, text="Due Date:").grid(row=3, column=0, padx=5, pady=5)
        self.due_date_entry = tk.Entry(self)
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.due_date_entry.insert(0, initial_values["dueDate"])

        tk.Label(self, text="Return Date:").grid(row=4, column=0, padx=5, pady=5)
        self.return_date_entry = tk.Entry(self)
        self.return_date_entry.grid(row=4, column=1, padx=5, pady=5)
        self.return_date_entry.insert(0, initial_values["returnDate"])

        # ok/cancel buttons
        tk.Button(self, text="OK", command=self.on_ok).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Status:").grid(row=5, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(self)
        self.status_var.set("open")  # Default status
        self.status_dropdown = ttk.Combobox(self, textvariable=self.status_var, values=["open", "close", "delay"])
        self.status_dropdown.grid(row=5, column=1, padx=5, pady=5)

        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    #ok button pressed
    def on_ok(self):
        book_id = self.book_id_entry.get().strip()
        members_id = self.members_id_entry.get().strip()
        loan_date = self.loan_date_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        return_date = self.return_date_entry.get().strip()
        status = self.status_var.get().strip()

        #if a field is empty
        if not book_id or not members_id or not loan_date or not due_date or not status:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Check if return date is empty/none
        if return_date.lower() == 'none' or not return_date:
            return_date = None

        self.result = {"bookID": book_id, "membersID": members_id, "loanDate": loan_date,
                       "dueDate": due_date, "returnDate": return_date, "status": status}
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

#Loan management window
class LoanManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Loan Management System")

        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "BookID", "MembersID", "LoanDate", "DueDate", "ReturnDate", "Status"), show="headings")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        #table headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MembersID", text="MembersID")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.heading("DueDate", text="DueDate")
        self.tree.heading("ReturnDate", text="ReturnDate")
        self.tree.heading("Status", text="Status")

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        window.grid_columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text="Search", command=self.open_search_dialog).grid(row=0, column=4, padx=5, pady=5,
                                                                                   sticky='ew')
        btn_frame.grid_columnconfigure(4, weight=1)

        # buttons names & action
        button_labels = ['Add Loan', 'Update Loan', 'Refresh']
        actions = [self.add_loan, self.update_loan, self.refresh_loan_list]

        # create buttons with text labels and assign actions
        for i, (label, action) in enumerate(zip(button_labels, actions)):
            ttk.Button(btn_frame, text=label, command=action).grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)

        self.refresh_loan_list()

    # add,update,refresh,search
    def refresh_loan_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loan in DatabaseManager.get_loan():
            self.tree.insert('', 'end', values=(loan.id, loan.bookID, loan.membersID, loan.loanDate, loan.dueDate, loan.returnDate, loan.status))

    def search_loan(self, query):
        if query:
            found_loan = DatabaseManager.search_loan(query)
            self.update_view(found_loan)
        else:
            messagebox.showwarning("Warning", "Please enter a search query.")

    def open_search_dialog(self):
        dialog = SearchDialog(self.window, "Search Loan")
        query = dialog.show()
        if query:  # Check if query is not None
            self.search_loan(query)

    def update_view(self, loans):
        self.tree.delete(*self.tree.get_children())

        #columns names
        self.tree.config(columns=("ID", "BookID", "MembersID", "LoanDate", "DueDate", "ReturnDate", "Status"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MembersID", text="MembersID")
        self.tree.heading("LoanDate", text="Loan Date")
        self.tree.heading("DueDate", text="Due Date")
        self.tree.heading("ReturnDate", text="Return Date")
        self.tree.heading("Status", text="Status")

        #insert new loan data
        for loan in loans:
            self.tree.insert('', 'end', values=(
                loan.id, loan.bookID, loan.membersID, loan.loanDate, loan.dueDate, loan.returnDate, loan.status))

    def add_loan(self):
        dialog = LoanDialog(self.window, "Add Loan")
        result = dialog.show()
        if result:  # Check if result is not None
            loan = Loan(result["bookID"], result["membersID"], result["loanDate"], result["dueDate"], result["returnDate"], result["status"])
            DatabaseManager.add_loan(loan)
            self.refresh_loan_list()

    def update_loan(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"bookID": item[1], "membersID": item[2], "loanDate": item[3],
                              "dueDate": item[4], "returnDate": item[5], "status": item[6]}
            dialog = LoanDialog(self.window, "Update Loan", initial_values)
            result = dialog.show()
            if result:
                # Check if return date is empty/none
                return_date = result["returnDate"] if result["returnDate"] else None

                loan = Loan(result["bookID"], result["membersID"], result["loanDate"],
                            result["dueDate"], return_date, result["status"], item[0])
                DatabaseManager.update_loan(loan)
                self.refresh_loan_list()
        else:
            messagebox.showwarning("Warning", "Please select a loan to update.")


#search window popup
class SearchDialog(tk.Toplevel):
    def __init__(self, parent, title="Search Loan"):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        # search field & button
        tk.Label(self, text="Enter keyword:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.insert(0, "write something")  # Set the hint text
        self.search_entry.config(fg='grey')  # Set hint text color to grey
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        tk.Button(self, text="Search", command=self.on_search).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def on_entry_click(self, event):
        if self.search_entry.get() == "write something":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg='black')

    def on_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "write something")
            self.search_entry.config(fg='grey')

    def on_search(self):
        query = self.search_entry.get().strip()
        if query and query != "write something":
            self.result = query
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter a search query.")

    def show(self):
        self.wait_window()
        return self.result


if __name__ == "__main__":
    root = tk.Tk()
    app = LoanManagementGUI(root)
    root.mainloop()
