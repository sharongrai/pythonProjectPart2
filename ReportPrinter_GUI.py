import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from ReportPrinter import DatabaseManager  # Assuming you have implemented this module

class ReportPrinterGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Report Printer")

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Initialize GUI components
        self.init_gui()

    def init_gui(self):
        # Label and Combobox for report type selection
        ttk.Label(self.frame, text="Select Report Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.report_type_combobox = ttk.Combobox(self.frame, values=["Loan Report", "Return Report", "Popular Books Report"])
        self.report_type_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.report_type_combobox.current(0)

        # Radio buttons for selecting date range or month & year
        self.report_option = tk.IntVar()
        ttk.Radiobutton(self.frame, text="By Date Range", variable=self.report_option, value=1).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)


        # Fields for date range
        ttk.Label(self.frame, text="Start Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_entry = ttk.Entry(self.frame)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.start_date_entry.insert(tk.END, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(self.frame, text="End Date:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_date_entry = ttk.Entry(self.frame)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.end_date_entry.insert(tk.END, datetime.now().strftime("%Y-%m-%d"))

        ttk.Radiobutton(self.frame, text="By Month & Year", variable=self.report_option, value=2).grid(row=4, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky=tk.W)
        # Fields for month & year selection
        ttk.Label(self.frame, text="Month:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.month_combobox = ttk.Combobox(self.frame, values=[i for i in range(1, 13)])
        self.month_combobox.grid(row=5, column=1, padx=5, pady=5)
        self.month_combobox.current(0)

        ttk.Label(self.frame, text="Year:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.year_combobox = ttk.Combobox(self.frame, values=[2022, 2023, 2024])
        self.year_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.year_combobox.current(0)

        # Button to generate report
        ttk.Button(self.frame, text="Generate Report", command=self.generate_report).grid(row=7, columnspan=2, padx=5, pady=5)

    def generate_report(self):
        report_type = self.report_type_combobox.get()
        option = self.report_option.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()

        report = DatabaseManager.generate_report(report_type, option, start_date, end_date, month, year)

        # Open new window to display report
        self.display_window = tk.Toplevel(self.parent)
        self.display_window.title("Report")

        # Frame for Treeview and Scrollbar
        tree_frame = ttk.Frame(self.display_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview setup
        tree = ttk.Treeview(tree_frame, columns=("ID", "BookID", "MembersID", "LoanDate", "DueDate", "ReturnDate", "Status"), show="headings")
        tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscroll=scrollbar.set)

        tree.heading("ID", text="ID")
        tree.heading("BookID", text="Book ID")
        tree.heading("MembersID", text="Member's ID")
        tree.heading("LoanDate", text="Loan Date")
        tree.heading("DueDate", text="Due Date")
        tree.heading("ReturnDate", text="Return Date")
        tree.heading("Status", text="Status")

        # Display report in Treeview
        self.display_report(report, tree)

    def display_report(self, report, tree):
        if isinstance(report, list) and len(report) > 0:
            # Insert column headers
            headers = ("Loan ID", "Book ID", "Member ID", "Loan Date", "Due Date", "Return Date", "Status")
            tree.heading("#0", text="Index")
            for col, header in enumerate(headers):
                tree.heading(col, text=header)

            # Insert loan records as rows
            for idx, loan in enumerate(report):
                tree.insert("", tk.END, text=idx, values=loan)
        else:
            tree.insert("", tk.END, text="No loan records found for the selected period.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportPrinterGUI(root)
    root.mainloop()
