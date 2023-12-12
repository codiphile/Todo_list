import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Create a MySQL connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='todolist'
)

# Create a cursor object to interact with the database
cursor = db.cursor()

def get_max_task_id():
    cursor.execute("SELECT MAX(id) FROM tasks")
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def add_task():
    task_name = task_name_entry.get()
    description = description_entry.get()
    
    if task_name:
        max_id = get_max_task_id()
        new_id = max_id + 1
        cursor.execute("INSERT INTO tasks (id, task_name, description) VALUES (%s, %s, %s)",
                       (new_id, task_name, description))
        db.commit()
        refresh_list()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "Please enter a task name.")

def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return tasks

def clear_entries():
    task_name_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def update_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_id = int(selected_task.split(':')[0])
        task_name = task_name_entry.get()
        description = description_entry.get()
        if task_name:
            cursor.execute("UPDATE tasks SET task_name = %s, description = %s WHERE id = %s",
                           (task_name, description, task_id))
            db.commit()
            refresh_list()
            clear_entries()
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")
    else:
        messagebox.showwarning("Warning", "Please select a task to update.")

def mark_task_completed():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_id = int(selected_task.split(':')[0])
        cursor.execute("UPDATE tasks SET is_completed = TRUE WHERE id = %s", (task_id,))
        db.commit()
        refresh_list()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as complete.")

def delete_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_id = int(selected_task.split(':')[0])
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.commit()
        refresh_list()
    else:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def refresh_list():
    task_list.delete(0, tk.END)
    tasks = view_tasks()
    for task in tasks:
        task_list.insert(tk.END, f"{task[0]}: {task[1]} - {task[2]} {'(Completed)' if task[3] else ''}")

# Create the main window
root = tk.Tk()
root.title("To-Do List App")

# Labels and Entry widgets for task name and description
task_name_label = tk.Label(root, text="Task Name:")
task_name_label.pack()
task_name_entry = tk.Entry(root, width=40)
task_name_entry.pack()

description_label = tk.Label(root, text="Description:")
description_label.pack()
description_entry = tk.Entry(root, width=40)
description_entry.pack()

# Buttons for adding, updating, marking as complete, deleting, and refreshing tasks
add_button = tk.Button(root, text="Add Task", command=add_task)
update_button = tk.Button(root, text="Update Task", command=update_task)
mark_completed_button = tk.Button(root, text="Mark as Complete", command=mark_task_completed)
delete_button = tk.Button(root, text="Delete Task", command=delete_task)
refresh_button = tk.Button(root, text="Refresh List", command=refresh_list)

add_button.pack()
update_button.pack()
mark_completed_button.pack()
delete_button.pack()
refresh_button.pack()

# Listbox to display tasks
task_list = tk.Listbox(root, width=60)
task_list.pack()

# Initial display of tasks
refresh_list()

root.mainloop()

# Close the database connection when the application is closed
cursor.close()
db.close()
