from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

# DB connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="Fresher@15",
    database="library"
)
cur = con.cursor()

# Table names
issueTable = "issued_books"
bookTable = "books"

allBid = []  # store all Book IDs


def issue():
    global root, inf1, inf2

    bid = inf1.get().strip()
    sid = inf2.get().strip()

    if not bid or not sid:
        messagebox.showwarning("Input error", "Please enter both Book ID and Student ID.")
        return

    try:
        # Fetch all book IDs
        cur.execute(f"SELECT bid FROM {bookTable}")
        allBid.clear()
        for row in cur:
            allBid.append(str(row[0]))

        if bid not in allBid:
            messagebox.showinfo("Error", "Book ID not found in library.")
            return

        # Check status
        cur.execute(f"SELECT status FROM {bookTable} WHERE bid = %s", (bid,))
        row = cur.fetchone()
        if not row:
            messagebox.showinfo("Error", "Book ID not found.")
            return

        status_value = row[0].lower()
        if status_value != "avail":
            messagebox.showinfo("Message", "Book is already issued.")
            return

        # ✅ Insert into issued_books (issued_id auto, return_date NULL, issue_date = NOW())
        insert_sql = f"""
            INSERT INTO {issueTable} (bid, sid, issue_date)
            VALUES (%s, %s, NOW())
        """
        cur.execute(insert_sql, (bid, sid))
        con.commit()

        # Update status in books table
        cur.execute(f"UPDATE {bookTable} SET status = 'issued' WHERE bid = %s", (bid,))
        con.commit()

        messagebox.showinfo("Success", "Book Issued Successfully ✅")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        allBid.clear()


def issueBook():
    global root, inf1, inf2

    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root, bg="#D6ED17")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(
        headingFrame1,
        text="Issue Book",
        bg='black',
        fg='white',
        font=('Courier', 15)
    )
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Book ID
    Label(labelFrame, text="Book ID : ", bg='black', fg='white').place(relx=0.05, rely=0.2)
    inf1 = Entry(labelFrame)
    inf1.place(relx=0.3, rely=0.2, relwidth=0.62)

    # Student ID
    Label(labelFrame, text="Student ID : ", bg='black', fg='white').place(relx=0.05, rely=0.4)
    inf2 = Entry(labelFrame)
    inf2.place(relx=0.3, rely=0.4, relwidth=0.62)

    # Buttons
    Button(root, text="Issue", bg='#d1ccc0', fg='black', command=issue).place(
        relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08
    )
    Button(root, text="Quit", bg='#aaa69d', fg='black', command=root.destroy).place(
        relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08
    )

    root.mainloop()
