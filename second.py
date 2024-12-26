import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Database setup
def initialize_db():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Publisher (
                            PublisherID INTEGER PRIMARY KEY,
                            PublisherName TEXT NOT NULL,
                            Address TEXT,
                            ContactNumber TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Book (
                            Book_ID INTEGER PRIMARY KEY,
                            Title TEXT,
                            Author TEXT,
                            ISBN TEXT UNIQUE,
                            Publisher TEXT,
                            Year_Published INTEGER,
                       PublisherID INTEGER NOT NULL,
                            Category TEXT,
                            Copies_Available INTEGER,
                        FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Member (
                            Member_ID INTEGER PRIMARY KEY,
                            Name TEXT,
                            Email TEXT UNIQUE,
                            Phone TEXT,
                            Address TEXT,
                            Registration_Date TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Borrow (
                            Transaction_ID INTEGER PRIMARY KEY,
                            Member_ID INTEGER,
                            Book_ID INTEGER,
                            Borrow_Date TEXT,
                            Return_Date TEXT,
                            Fine REAL,
                            FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID),
                            FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID))""")
        conn.commit()

# GUI setup
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#F0F8FF")  # to change the colour of background to blue

        # Title Label
        title_label = tk.Label(self.root, text="Library Management System", bg="#4682B4", fg="white", font=("Arial", 20, "bold"))
        title_label.pack(fill=tk.X)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.setup_book_tab()
        self.setup_member_tab()
        self.setup_borrow_tab()

    def setup_book_tab(self):
        book_tab = tk.Frame(self.notebook, bg="#F5FFFA")
        self.notebook.add(book_tab, text="Books")

        # Book Form
        form_frame = tk.Frame(book_tab, bg="#F5FFFA", pady=10)
        form_frame.pack(fill=tk.X, padx=10)

        tk.Label(form_frame, text="Title:", bg="#F5FFFA").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_title_entry = tk.Entry(form_frame)
        self.book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Author:", bg="#F5FFFA").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_author_entry = tk.Entry(form_frame)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="ISBN:", bg="#F5FFFA").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_isbn_entry = tk.Entry(form_frame)
        self.book_isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Publisher:", bg="#F5FFFA").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_publisher_entry = tk.Entry(form_frame)
        self.book_publisher_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Year Published:", bg="#F5FFFA").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_year_entry = tk.Entry(form_frame)
        self.book_year_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Category:", bg="#F5FFFA").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_category_entry = tk.Entry(form_frame)
        self.book_category_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Copies Available:", bg="#F5FFFA").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_copies_entry = tk.Entry(form_frame)
        self.book_copies_entry.grid(row=6, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(book_tab, bg="#F5FFFA", pady=10)
        button_frame.pack(fill=tk.X, padx=10)

        add_button = tk.Button(button_frame, text="Add Book", command=self.add_book, bg="#32CD32", fg="white", font=("Arial", 10, "bold"))
        add_button.pack(side=tk.LEFT, padx=5)

        view_button = tk.Button(button_frame, text="View Books", command=self.view_books, bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
        view_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Book", command=self.delete_book, bg="#FF6347", fg="white", font=("Arial", 10, "bold"))
        delete_button.pack(side=tk.LEFT, padx=5)

        # Table
        self.book_table = ttk.Treeview(book_tab, columns=("ID", "Title", "Author", "Copies"), show="headings")
        self.book_table.heading("ID", text="ID")
        self.book_table.heading("Title", text="Title")
        self.book_table.heading("Author", text="Author")
        self.book_table.heading("Copies", text="Copies")
        self.book_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        publisher = self.book_publisher_entry.get()
        year = self.book_year_entry.get()
        category = self.book_category_entry.get()
        copies = self.book_copies_entry.get()

        if not title or not author or not isbn or not copies:
            messagebox.showerror("Error", "Please fill out all required fields.")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Book (Title, Author, ISBN, Publisher, Year_Published, Category, Copies_Available) VALUES (?, ?, ?, ?, ?, ?, ?) ",
                               (title, author, isbn, publisher, year, category, copies))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Error", f"{e}")

    def view_books(self):
        for row in self.book_table.get_children():
            self.book_table.delete(row)

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Book_ID, Title, Author, Copies_Available FROM Book")
            books = cursor.fetchall()

        for book in books:
            self.book_table.insert("", "end", values=book)

    def delete_book(self):
        selected_item = self.book_table.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a book to delete.")
            return

        book_id = self.book_table.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the book with ID {book_id}?")
        if confirm:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Book WHERE Book_ID = ?", (book_id,))
                conn.commit()

            messagebox.showinfo("Success", "Book deleted successfully!")
            self.view_books()

    def setup_member_tab(self):
        member_tab = tk.Frame(self.notebook, bg="#FFF5EE")
        self.notebook.add(member_tab, text="Members")

        # Member Form
        form_frame = tk.Frame(member_tab, bg="#FFF5EE", pady=10)
        form_frame.pack(fill=tk.X, padx=10)

        tk.Label(form_frame, text="Name:", bg="#FFF5EE").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_name_entry = tk.Entry(form_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg="#FFF5EE").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_email_entry = tk.Entry(form_frame)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Phone:", bg="#FFF5EE").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_phone_entry = tk.Entry(form_frame)
        self.member_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Address:", bg="#FFF5EE").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.member_address_entry = tk.Entry(form_frame)
        self.member_address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(member_tab, bg="#FFF5EE", pady=10)
        button_frame.pack(fill=tk.X, padx=10)

        add_member_button = tk.Button(button_frame, text="Add Member", command=self.add_member, bg="#32CD32", fg="white", font=("Arial", 10, "bold"))
        add_member_button.pack(side=tk.LEFT, padx=5)

        view_members_button = tk.Button(button_frame, text="View Members", command=self.view_members, bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
        view_members_button.pack(side=tk.LEFT, padx=5)

        delete_member_button = tk.Button(button_frame, text="Delete Member", command=self.delete_member, bg="#FF6347", fg="white", font=("Arial", 10, "bold"))
        delete_member_button.pack(side=tk.LEFT, padx=5)

        # Table
        self.member_table = ttk.Treeview(member_tab, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.member_table.heading("ID", text="ID")
        self.member_table.heading("Name", text="Name")
        self.member_table.heading("Email", text="Email")
        self.member_table.heading("Phone", text="Phone")
        self.member_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        phone = self.member_phone_entry.get()
        address = self.member_address_entry.get()

        if not name or not email or not phone:
            messagebox.showerror("Error", "Please fill out all required fields.")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Member (Name, Email, Phone, Address, Registration_Date) VALUES (?, ?, ?, ?, ?)",
                               (name, email, phone, address, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                messagebox.showinfo("Success", "Member added successfully!")
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Error", f"{e}")

    def view_members(self):
        for row in self.member_table.get_children():
            self.member_table.delete(row)

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Member_ID, Name, Email, Phone FROM Member")
            members = cursor.fetchall()

        for member in members:
            self.member_table.insert("", "end", values=member)

    def delete_member(self):
        selected_item = self.member_table.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a member to delete.")
            return

        member_id = self.member_table.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the member with ID {member_id}?")
        if confirm:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Member WHERE Member_ID = ?", (member_id,))
                conn.commit()

            messagebox.showinfo("Success", "Member deleted successfully!")
            self.view_members()

    def setup_borrow_tab(self):
        borrow_tab = tk.Frame(self.notebook, bg="#FAFAD2")
        self.notebook.add(borrow_tab, text="Borrow/Return")

        # Borrow Form
        form_frame = tk.Frame(borrow_tab, bg="#FAFAD2", pady=10)
        form_frame.pack(fill=tk.X, padx=10)

        tk.Label(form_frame, text="Member ID:", bg="#FAFAD2").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.borrow_member_id_entry = tk.Entry(form_frame)
        self.borrow_member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Book ID:", bg="#FAFAD2").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.borrow_book_id_entry = tk.Entry(form_frame)
        self.borrow_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Borrow Date (YYYY-MM-DD):", bg="#FAFAD2").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.borrow_date_entry = tk.Entry(form_frame)
        self.borrow_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Return Date (YYYY-MM-DD):", bg="#FAFAD2").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.return_date_entry = tk.Entry(form_frame)
        self.return_date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(borrow_tab, bg="#FAFAD2", pady=10)
        button_frame.pack(fill=tk.X, padx=10)

        borrow_button = tk.Button(button_frame, text="Borrow Book", command=self.borrow_book, bg="#32CD32", fg="white", font=("Arial", 10, "bold"))
        borrow_button.pack(side=tk.LEFT, padx=5)

        return_button = tk.Button(button_frame, text="Return Book", command=self.return_book, bg="#FF6347", fg="white", font=("Arial", 10, "bold"))
        return_button.pack(side=tk.LEFT, padx=5)

        view_borrowed_button = tk.Button(button_frame, text="View Borrowed Books", command=self.view_borrowed_books, bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
        view_borrowed_button.pack(side=tk.LEFT, padx=5)

        # Borrowed Books Table
        self.borrow_table = ttk.Treeview(borrow_tab, columns=("Transaction ID", "Member Name", "Book Title", "Borrow Date", "Return Date", "Fine"), show="headings")
        self.borrow_table.heading("Transaction ID", text="Transaction ID")
        self.borrow_table.heading("Member Name", text="Member Name")
        self.borrow_table.heading("Book Title", text="Book Title")
        self.borrow_table.heading("Borrow Date", text="Borrow Date")
        self.borrow_table.heading("Return Date", text="Return Date")
        self.borrow_table.heading("Fine", text="Fine")
        self.borrow_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def view_borrowed_books(self):
        for row in self.borrow_table.get_children():
            self.borrow_table.delete(row)

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Borrow.Transaction_ID, Member.Name, Book.Title, Borrow.Borrow_Date, Borrow.Return_Date, Borrow.Fine
                FROM Borrow
                JOIN Member ON Borrow.Member_ID = Member.Member_ID
                JOIN Book ON Borrow.Book_ID = Book.Book_ID
            """)
            borrowed_books = cursor.fetchall()

        for book in borrowed_books:
            self.borrow_table.insert("", "end", values=book)

    def borrow_book(self):
        member_id = self.borrow_member_id_entry.get()
        book_id = self.borrow_book_id_entry.get()
        borrow_date = self.borrow_date_entry.get()
        return_date = self.return_date_entry.get()

        if not member_id or not book_id or not borrow_date or not return_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Borrow (Member_ID, Book_ID, Borrow_Date, Return_Date) VALUES (?, ?, ?, ?)",
                           (member_id, book_id, borrow_date, return_date))
            conn.commit()
            messagebox.showinfo("Success", "Book borrowed successfully!")

    def return_book(self):
        member_id = self.borrow_member_id_entry.get()
        book_id = self.borrow_book_id_entry.get()

        if not member_id or not book_id:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        return_date = self.return_date_entry.get()

        if not return_date:
            messagebox.showerror("Error", "Please enter the return date.")
            return

        # Convert string dates to datetime objects for comparison
        try:
            return_date = datetime.strptime(return_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid return date format. Use YYYY-MM-DD.")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()

            # Fetch the expected return date from the Borrow table
            cursor.execute("SELECT Return_Date FROM Borrow WHERE Member_ID = ? AND Book_ID = ?", (member_id, book_id))
            result = cursor.fetchone()

            if result:
                expected_return_date = datetime.strptime(result[0], "%Y-%m-%d")

                # Calculate fine if the return date is later than the expected return date
                fine = 0
                if return_date > expected_return_date:
                    delta = return_date - expected_return_date
                    fine = delta.days * 0.5  # Example: $0.5 per day overdue

                # Update the Borrow table with the return date and fine
                cursor.execute("UPDATE Borrow SET Return_Date = ?, Fine = ? WHERE Member_ID = ? AND Book_ID = ?",
                               (return_date.strftime("%Y-%m-%d"), fine, member_id, book_id))
                conn.commit()

                messagebox.showinfo("Success", f"Book returned successfully! Fine: ${fine:.2f}")
            else:
                messagebox.showerror("Error", "No borrowing record found for this member and book.")


# Main function to run the app
if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
