import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name TEXT,
    branch TEXT,
    year TEXT,
    email TEXT
)
""")
conn.commit()

# ---------- Functions ----------
def add_student():
    roll_no = entry_roll.get()
    name = entry_name.get()
    branch = entry_branch.get()
    year = entry_year.get()
    email = entry_email.get()
    
    if roll_no == "" or name == "":
        messagebox.showerror("Error", "Roll No & Name are required!")
        return
    
    try:
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", 
                       (roll_no, name, branch, year, email))
        conn.commit()
        messagebox.showinfo("Success", "Student Added Successfully")
        fetch_students()
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll No already exists!")

def fetch_students():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a student to delete")
        return
    roll_no = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()
    fetch_students()
    messagebox.showinfo("Deleted", "Student Record Deleted")

def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_branch.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# ---------- UI Setup ----------
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")

# Input Frame
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Roll No").grid(row=0, column=0)
tk.Label(frame_input, text="Name").grid(row=1, column=0)
tk.Label(frame_input, text="Branch").grid(row=2, column=0)
tk.Label(frame_input, text="Year").grid(row=3, column=0)
tk.Label(frame_input, text="Email").grid(row=4, column=0)

entry_roll = tk.Entry(frame_input)
entry_name = tk.Entry(frame_input)
entry_branch = tk.Entry(frame_input)
entry_year = tk.Entry(frame_input)
entry_email = tk.Entry(frame_input)

entry_roll.grid(row=0, column=1, padx=5, pady=5)
entry_name.grid(row=1, column=1, padx=5, pady=5)
entry_branch.grid(row=2, column=1, padx=5, pady=5)
entry_year.grid(row=3, column=1, padx=5, pady=5)
entry_email.grid(row=4, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Add Student", command=add_student).grid(row=5, column=0, pady=10)
tk.Button(frame_input, text="Delete Student", command=delete_student).grid(row=5, column=1, pady=10)
tk.Button(frame_input, text="Clear", command=clear_fields).grid(row=5, column=2, pady=10)

# Data Display
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True)

columns = ("Roll No", "Name", "Branch", "Year", "Email")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

fetch_students()

root.mainloop()
