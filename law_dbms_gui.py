# law_dbms_gui.py
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "law_db.sqlite"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clients (
                    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    contact TEXT,
                    email TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS lawyers (
                    lawyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    specialization TEXT,
                    contact TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS cases (
                    case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    client_id INTEGER,
                    lawyer_id INTEGER,
                    status TEXT,
                    description TEXT,
                    FOREIGN KEY(client_id) REFERENCES clients(client_id),
                    FOREIGN KEY(lawyer_id) REFERENCES lawyers(lawyer_id))""")
    conn.commit()
    conn.close()

# GUI App
class LawDBMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Law DBMS - Frontend GUI")
        self.root.geometry("900x600")

        self.tabControl = ttk.Notebook(root)
        self.client_tab = ttk.Frame(self.tabControl)
        self.lawyer_tab = ttk.Frame(self.tabControl)
        self.case_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.client_tab, text="Clients")
        self.tabControl.add(self.lawyer_tab, text="Lawyers")
        self.tabControl.add(self.case_tab, text="Cases")
        self.tabControl.pack(expand=1, fill="both")

        self.setup_client_tab()
        self.setup_lawyer_tab()
        self.setup_case_tab()

    # --- CLIENT TAB ---
    def setup_client_tab(self):
        frame = ttk.Frame(self.client_tab, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Client Name:").grid(row=0, column=0)
        ttk.Label(frame, text="Contact:").grid(row=1, column=0)
        ttk.Label(frame, text="Email:").grid(row=2, column=0)

        self.client_name = tk.Entry(frame)
        self.client_contact = tk.Entry(frame)
        self.client_email = tk.Entry(frame)
        self.client_name.grid(row=0, column=1)
        self.client_contact.grid(row=1, column=1)
        self.client_email.grid(row=2, column=1)

        ttk.Button(frame, text="Add Client", command=self.add_client).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Refresh", command=self.refresh_clients).grid(row=3, column=1, pady=5)

        self.client_tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact", "Email"), show="headings")
        for col in self.client_tree["columns"]:
            self.client_tree.heading(col, text=col)
        self.client_tree.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.refresh_clients()

    def add_client(self):
        name = self.client_name.get()
        contact = self.client_contact.get()
        email = self.client_email.get()
        if not name:
            messagebox.showerror("Error", "Client name required")
            return
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO clients (name, contact, email) VALUES (?, ?, ?)", (name, contact, email))
        conn.commit()
        conn.close()
        self.refresh_clients()
        messagebox.showinfo("Success", "Client added successfully!")

    def refresh_clients(self):
        for i in self.client_tree.get_children():
            self.client_tree.delete(i)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients")
        for row in cur.fetchall():
            self.client_tree.insert("", "end", values=row)
        conn.close()

    # --- LAWYER TAB ---
    def setup_lawyer_tab(self):
        frame = ttk.Frame(self.lawyer_tab, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Lawyer Name:").grid(row=0, column=0)
        ttk.Label(frame, text="Specialization:").grid(row=1, column=0)
        ttk.Label(frame, text="Contact:").grid(row=2, column=0)

        self.lawyer_name = tk.Entry(frame)
        self.lawyer_specialization = tk.Entry(frame)
        self.lawyer_contact = tk.Entry(frame)
        self.lawyer_name.grid(row=0, column=1)
        self.lawyer_specialization.grid(row=1, column=1)
        self.lawyer_contact.grid(row=2, column=1)

        ttk.Button(frame, text="Add Lawyer", command=self.add_lawyer).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Refresh", command=self.refresh_lawyers).grid(row=3, column=1, pady=5)

        self.lawyer_tree = ttk.Treeview(frame, columns=("ID", "Name", "Specialization", "Contact"), show="headings")
        for col in self.lawyer_tree["columns"]:
            self.lawyer_tree.heading(col, text=col)
        self.lawyer_tree.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.refresh_lawyers()

    def add_lawyer(self):
        name = self.lawyer_name.get()
        specialization = self.lawyer_specialization.get()
        contact = self.lawyer_contact.get()
        if not name:
            messagebox.showerror("Error", "Lawyer name required")
            return
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO lawyers (name, specialization, contact) VALUES (?, ?, ?)", (name, specialization, contact))
        conn.commit()
        conn.close()
        self.refresh_lawyers()
        messagebox.showinfo("Success", "Lawyer added successfully!")

    def refresh_lawyers(self):
        for i in self.lawyer_tree.get_children():
            self.lawyer_tree.delete(i)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM lawyers")
        for row in cur.fetchall():
            self.lawyer_tree.insert("", "end", values=row)
        conn.close()

    # --- CASE TAB ---
    def setup_case_tab(self):
        frame = ttk.Frame(self.case_tab, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Case Title:").grid(row=0, column=0)
        ttk.Label(frame, text="Client ID:").grid(row=1, column=0)
        ttk.Label(frame, text="Lawyer ID:").grid(row=2, column=0)
        ttk.Label(frame, text="Status:").grid(row=3, column=0)
        ttk.Label(frame, text="Description:").grid(row=4, column=0)

        self.case_title = tk.Entry(frame)
        self.case_client_id = tk.Entry(frame)
        self.case_lawyer_id = tk.Entry(frame)
        self.case_status = tk.Entry(frame)
        self.case_description = tk.Entry(frame)
        self.case_title.grid(row=0, column=1)
        self.case_client_id.grid(row=1, column=1)
        self.case_lawyer_id.grid(row=2, column=1)
        self.case_status.grid(row=3, column=1)
        self.case_description.grid(row=4, column=1)

        ttk.Button(frame, text="Add Case", command=self.add_case).grid(row=5, column=0, pady=5)
        ttk.Button(frame, text="Refresh", command=self.refresh_cases).grid(row=5, column=1, pady=5)

        self.case_tree = ttk.Treeview(frame, columns=("ID", "Title", "Client", "Lawyer", "Status", "Description"), show="headings")
        for col in self.case_tree["columns"]:
            self.case_tree.heading(col, text=col)
        self.case_tree.grid(row=6, column=0, columnspan=3, sticky="nsew")

        self.refresh_cases()

    def add_case(self):
        title = self.case_title.get()
        client_id = self.case_client_id.get()
        lawyer_id = self.case_lawyer_id.get()
        status = self.case_status.get()
        description = self.case_description.get()
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO cases (title, client_id, lawyer_id, status, description) VALUES (?, ?, ?, ?, ?)",
                    (title, client_id, lawyer_id, status, description))
        conn.commit()
        conn.close()
        self.refresh_cases()
        messagebox.showinfo("Success", "Case added successfully!")

    def refresh_cases(self):
        for i in self.case_tree.get_children():
            self.case_tree.delete(i)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM cases")
        for row in cur.fetchall():
            self.case_tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LawDBMS(root)
    root.mainloop()
