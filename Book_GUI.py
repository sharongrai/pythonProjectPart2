import functools
import tkinter as tk
from tkinter import messagebox, ttk
from Book import Book, DatabaseManager

#add book window
class BookDialog(tk.Toplevel):
    def __init__(self, parent, title="Book Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"title": "", "author": "", "genre": "", "year": "", "shelfLocation": "", "status": ""}

        self.result = None

        # add book fields
        tk.Label(self, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.insert(0, initial_values["title"])

        tk.Label(self, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        self.author_entry.insert(0, initial_values["author"])

        tk.Label(self, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)
        self.genre_entry.insert(0, initial_values["genre"])

        tk.Label(self, text="Year:").grid(row=3, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5)
        self.year_entry.insert(0, initial_values["year"])

        tk.Label(self, text="Shelf Location:").grid(row=4, column=0, padx=5, pady=5)
        self.shelfLocation_entry = tk.Entry(self)
        self.shelfLocation_entry.grid(row=4, column=1, padx=5, pady=5)
        self.shelfLocation_entry.insert(0, initial_values["shelfLocation"])

        tk.Label(self, text="Status:").grid(row=5, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(self)
        self.status_var.set("available")  # Default status
        self.status_dropdown = ttk.Combobox(self, textvariable=self.status_var, values=["available", "unavailable"])
        self.status_dropdown.grid(row=5, column=1, padx=5, pady=5)

        # ok/cancel buttons
        tk.Button(self, text="OK", command=self.on_ok).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=6, column=1, padx=5, pady=5)

        self.grab_set()  # Make window modal
        self.wait_visibility()
        self.focus_set()

    def on_ok(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        shelfLocation = self.shelfLocation_entry.get().strip()
        status = self.status_var.get().strip()

        #if a field is empty
        if not title or not author or not genre or not year or not shelfLocation or not status:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            year = int(year)  # verify year is a number
        except ValueError:
            messagebox.showerror("Error", "year must be a number.")
            return

        self.result = {"title": title, "author": author, "genre": genre, "year": year,"shelfLocation": shelfLocation, "status": status}
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

#books managment window
class BookManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Book Management System")

        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame,columns=("ID", "Title", "Author", "Genre", "Year", "Shelf Location", "Status"),show="headings")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        #table headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Shelf Location", text="Shelf Location")
        self.tree.heading("Status", text="Status")

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        window.grid_columnconfigure(0, weight=1)

        # buttons names & action
        button_labels = ['Add Book', 'Update Book', 'Delete Book', 'Refresh', 'Search', 'Show Unavailable Books','Register For Waiting List', 'Show Waiting List']
        actions = [self.add_book, self.update_book, self.delete_book, self.refresh_book_list, self.search_book,self.show_unavailable_books, self.register_waiting_list, self.show_waiting_list]

        # create buttons with text labels and assign actions
        for i, (label, action) in enumerate(zip(button_labels, actions)):
            ttk.Button(btn_frame, text=label, command=action).grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)

        self.refresh_book_list()


#add,update,delete,refresh,search,show unavailble,register to WL
    def update_view(self, books):
        self.tree.delete(*self.tree.get_children())
        for book in books:
            self.tree.insert('', 'end', values=(
            book.id, book.title, book.author, book.genre, book.year, book.shelfLocation, book.status))

    def add_book(self):
        dialog = BookDialog(self.window, "Add Book")
        result = dialog.show()
        if result:
            book = Book(**result)
            DatabaseManager.add_book(book)
            self.refresh_book_list()

    def update_book(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"title": item[1], "author": item[2], "genre": item[3],
                              "year": item[4], "shelfLocation": item[5], "status": item[6]}
            dialog = BookDialog(self.window, "Update Book", initial_values)
            result = dialog.show()
            if result:
                book = Book(**result, id=item[0])
                DatabaseManager.update_book(book)
                self.refresh_book_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to update.")

    def delete_book(self):
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0], 'values')[0]
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this book?")
            if confirmation:
                DatabaseManager.delete_book(book_id)
                self.refresh_book_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to delete.")

    def refresh_book_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in DatabaseManager.get_books():
            self.tree.insert('', 'end', values=(
            book.id, book.title, book.author, book.genre, book.year, book.shelfLocation, book.status))

    def search_book(self):
        query = self.open_search_dialog()
        if query:
            found_books = DatabaseManager.search_books(query)
            self.update_view(found_books)

    def show_unavailable_books(self):
        all_books = DatabaseManager.get_books()
        unavailable_books = [book for book in all_books if book.status == 'unavailable']
        self.update_view(unavailable_books)

    def register_waiting_list(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "please select a book.")
            return

        book_id = self.tree.item(selected_item[0], 'values')[0]
        book_title = self.tree.item(selected_item[0], 'values')[1]

        # check that the book is available
        status = self.tree.item(selected_item, 'values')[6]  # The status is at index 6
        if status != 'unavailable':
            messagebox.showwarning("Warning", "the selected book is not unavailable.")
            return

        #get the highest order number for selected book in the waiting list
        highest_order_number = DatabaseManager().get_highest_order_number(book_id)
        #increase the highest order numb by one
        order_number = highest_order_number + 1 if highest_order_number is not None else 1

        #get member ID
        member_id_window = tk.Toplevel(self.window)

        #memberID field and button
        member_id_label = tk.Label(member_id_window, text="Member ID: ")
        member_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        member_id_entry = tk.Entry(member_id_window)
        member_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        confirm_button = tk.Button(member_id_window, text="Confirm",command=functools.partial(self.on_ok_member_id, member_id_entry, member_id_window))
        confirm_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def on_ok_member_id(self, member_id_entry, member_id_window):
        member_id = member_id_entry.get().strip()
        if member_id:
            member_id_window.destroy()
            selected_item = self.tree.selection()
            book_id = self.tree.item(selected_item[0], 'values')[0]
            book_title = self.tree.item(selected_item[0], 'values')[1]
            print(member_id)
            if book_id:
                DatabaseManager().add_to_waiting_list(book_id, book_title, member_id)
            else:
                messagebox.showwarning("warning", "No book selected.")
        else:
            messagebox.showwarning("Warning", "Please enter a Member ID.")


    def show_waiting_list(self):
        dialog = WaitingListDialog(self.window)
        dialog.focus_set()
        dialog.grab_set()
        dialog.wait_window()


    def open_search_dialog(self):
        dialog = SearchDialog(self.window, "Search Book")
        return dialog.show()

#search window popup
class SearchDialog(tk.Toplevel):
    def __init__(self, parent, title="Search Book"):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        #search field & button
        tk.Label(self, text="Enter keyword:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.insert(0, "write something")  #hint text
        self.search_entry.config(fg='grey')  #hint text is gray
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        tk.Button(self, text="Search", command=self.on_search).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def on_entry_click(self, event):
        if self.search_entry.get() == "write something":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg='black')  # Change text color to black

    def on_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "write something")
            self.search_entry.config(fg='grey')  # Change text color to grey

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


#waiting list window
class WaitingListDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.title("Waiting List")

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(tree_frame, columns=( "BookID", "MemberID", "Title", "OrderNumber", "DateAdded"),show="headings")
        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)

        #table headings
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("OrderNumber", text="OrderNumber")
        self.tree.heading("DateAdded", text="DateAdded")

        delete_button = tk.Button(self, text="Delete", command=self.delete_entry)
        delete_button.pack(pady=5)

        self.refresh_waiting_list()

    def refresh_waiting_list(self):
        #clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        #get waiting list from the database
        database_manager = DatabaseManager()
        waiting_list = database_manager.get_waiting_list()
        for entry in waiting_list:
            self.tree.insert('', 'end', values=entry)

    def delete_entry(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item, 'values')[0]
            member_id = self.tree.item(selected_item, 'values')[1]
            DatabaseManager().remove_from_waiting_list(book_id, member_id)
            self.refresh_waiting_list()
        else:
            messagebox.showwarning("Warning", "Please select an entry to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagementGUI(root)
    root.mainloop()
