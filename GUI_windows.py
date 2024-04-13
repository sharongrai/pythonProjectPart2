from tkinter import *
import tkinter as tk

def add_book():
    add_books = Toplevel()
    add_books.title("add book")
    thisLabel=Label(add_books)


def open_waiting_list_window():
    waitingList = Toplevel()
    waitingList.title("waiting list")
    mylabel = Label (waitingList, text="unavailable books: ").pack()


root = Tk()
root.title("WellRead") #שם החלונית
root.configure(bg="lavenderblush") #קביעת צבע הרקע
root.iconbitmap(r"C:\Users\sharo\OneDrive - Yezreel Valley College\לימודים\שנה ג'\פייתון מתקדם\פרויקט 2\book logo.jpg")
available_books_button = tk.Button(root , text="waiting list", command=open_waiting_list_window).pack()


mainloop()