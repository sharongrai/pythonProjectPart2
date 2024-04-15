import tkinter as tk
from idlelib.search import SearchDialog
from tkinter import ttk, messagebox
from Member import Member, DatabaseManager, DatabaseConnection

#add member window
class MemberDialog(tk.Toplevel):
    def __init__(self, parent, title="Member Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"name": "", "email": "", "phone": "", "membership_type": "", "membership_start_date": ""}

        self.result = None

        # add member fields
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, initial_values["name"])

        tk.Label(self, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.insert(0, initial_values["email"])

        tk.Label(self, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.insert(0, initial_values["phone"])

        tk.Label(self, text="Membership Type:").grid(row=3, column=0, padx=5, pady=5)
        self.membership_type_entry = tk.Entry(self)
        self.membership_type_entry.grid(row=3, column=1, padx=5, pady=5)
        self.membership_type_entry.insert(0, initial_values["membership_type"])

        tk.Label(self, text="Membership start date:").grid(row=4, column=0, padx=5, pady=5)
        self.membership_start_date_entry = tk.Entry(self)
        self.membership_start_date_entry.grid(row=4, column=1, padx=5, pady=5)
        self.membership_start_date_entry.insert(0, initial_values["membership_start_date"])

        # ok/cancel buttons
        tk.Button(self, text="OK", command=self.on_ok).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=5, column=1, padx=5, pady=5)

        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def on_ok(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        membership_type = self.membership_type_entry.get().strip()
        membership_start_date = self.membership_start_date_entry.get().strip()

        if not name or not email or not phone or not membership_type:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.result = {"name": name, "email": email, "phone": phone, "membership_type": membership_type, "membership_start_date": membership_start_date}
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result


#members managment window
class MemberManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Member Management System")

        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "name", "email", "phone", "membership_type", "membership_start_date"), show="headings")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        #table headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("membership_type", text="Membership Type")
        self.tree.heading("membership_start_date", text="Membership Start Date")

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        window.grid_columnconfigure(0, weight=1)

        #buttons names & action
        button_labels = ['Add', 'Update', 'Delete', 'Refresh']
        actions = [self.add_member, self.update_member, self.delete_member, self.refresh_member_list]

        #create buttons with text labels and assign actions
        for i, (label, action) in enumerate(zip(button_labels, actions)):
            ttk.Button(btn_frame, text=label, command=action).grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)

        self.refresh_member_list()

    def refresh_member_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for member in DatabaseManager.get_members():
            self.tree.insert('', 'end', values=(member.id, member.name, member.email, member.phone, member.membership_type, member.membership_start_date))

    def add_member(self):
        dialog = MemberDialog(self.window, "Add Member")
        result = dialog.show()
        if result:
            member = Member(result["name"], result["email"], result["phone"], result["membership_type"],result["membership_start_date"])
            DatabaseManager.add_member(member)
            self.refresh_member_list()

    def update_member(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"name": item[1], "email": item[2], "phone": item[3], "membership_type": item[4], "membership_start_date": item[5]}
            dialog = MemberDialog(self.window, "Update Member", initial_values)
            result = dialog.show()
            #check if result is not none
            if result:
                member = Member(result["name"], result["email"], result["phone"], result["membership_type"],result["membership_start_date"], item[0])
                DatabaseManager.update_member(member)
                self.refresh_member_list()
        else:
            messagebox.showwarning("Warning", "Please select a member to update.")

    def delete_member(self):
        selected = self.tree.selection()
        if selected:
            member_id = self.tree.item(selected[0], 'values')[0]
            DatabaseManager.delete_member(member_id)
            self.refresh_member_list()
        else:
            messagebox.showwarning("Warning", "Please select a member to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemberManagementGUI(root)
    root.mainloop()
