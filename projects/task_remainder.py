import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import threading
import time

# ---------- Database Setup ----------
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    status TEXT,
    deadline TEXT
)
""")
conn.commit()

# ---------- Functions ----------
def add_task():
    task = entry_task.get()
    deadline = entry_deadline.get()

    if task == "":
        messagebox.showerror("Error", "Task cannot be empty!")
        return
    
    cursor.execute("INSERT INTO tasks (task, status, deadline) VALUES (?, ?, ?)",
                   (task, "Pending", deadline))
    conn.commit()
    fetch_tasks()
    entry_task.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)

def fetch_tasks():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a task to delete")
        return
    task_id = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    fetch_tasks()

def mark_done():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a task to mark as done")
        return
    task_id = tree.item(selected[0])['values'][0]
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", ("Completed", task_id))
    conn.commit()
    fetch_tasks()

def check_reminders():
    while True:
        cursor.execute("SELECT task, deadline FROM tasks WHERE status='Pending'")
        for row in cursor.fetchall():
            task, deadline = row
            if deadline:
                try:
                    deadline_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                    if datetime.datetime.now() >= deadline_time:
                        messagebox.showwarning("Reminder", f"Deadline reached for task: {task}")
                        cursor.execute("UPDATE tasks SET status=? WHERE task=?", ("Overdue", task))
                        conn.commit()
                        fetch_tasks()
                except:
                    pass
        time.sleep(60)  # check every 1 minute

# ---------- UI Setup ----------
root = tk.Tk()
root.title("To-Do List with Reminders")
root.geometry("700x500")

# Input Frame
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Task").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_input, text="Deadline (YYYY-MM-DD HH:MM)").grid(row=1, column=0, padx=5, pady=5)

entry_task = tk.Entry(frame_input, width=40)
entry_deadline = tk.Entry(frame_input, width=25)

entry_task.grid(row=0, column=1, padx=5, pady=5)
entry_deadline.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Add Task", command=add_task).grid(row=2, column=0, pady=10)
tk.Button(frame_input, text="Delete Task", command=delete_task).grid(row=2, column=1, pady=10)
tk.Button(frame_input, text="Mark Done", command=mark_done).grid(row=2, column=2, pady=10)

# Data Display
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True)

columns = ("ID", "Task", "Status", "Deadline")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)

fetch_tasks()

# Start reminder thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

root.mainloop()
