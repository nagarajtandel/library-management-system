from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

# Database connection
con = pymysql.connect(host="localhost", user="root", password="Fresher@15", database="library")
cur = con.cursor()
bookTable = "books"

def View():
    root = Tk()
    root.title("Library")
    root.config(bg="#12a4d9")
    root.geometry("600x500")

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="View Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Treeview style
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
    style.configure("Treeview.Heading", font=('Courier', 10, 'bold'))
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Ensure full area is used

    tree = ttk.Treeview(labelFrame, columns=("BID", "Title", "Author", "Status"), show="headings")
    
    # Add headings
    for col in ("BID", "Title", "Author", "Status"):
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Add striped row tags
    tree.tag_configure('oddrow', background='light grey')
    tree.tag_configure('evenrow', background='light blue')

    # Scrollbar
    scrollbar = Scrollbar(labelFrame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    # Fetch data
    try:
        cur.execute(f"SELECT * FROM {bookTable}")
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            if i % 2 == 0:
                tree.insert("", "end", values=row, tags=('evenrow',))
            else:
                tree.insert("", "end", values=row, tags=('oddrow',))
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to fetch books from database\n{e}")

    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    root.mainloop()
