from tkinter import simpledialog, messagebox
from tkinter import *
import commands

def populate_tasks_listbox(tasks_listbox, tasks):
    tasks_listbox.delete(0, END)
    for i, t in enumerate(tasks, start=1):
        tasks_listbox.insert(END, f"{i}. {t}")

def add_task(app, tasks_listbox, tasks):
    text = simpledialog.askstring('Add Task', 'Task:', parent=app)
    if not text or not text.strip():
        return
    
    tasks.append(text.strip())
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox, tasks)

def complete_task(tasks_listbox, timer_label, tasks):
    checked_indices = tasks_listbox.curselection()
    
    if not checked_indices:
        messagebox.showinfo('Complete Task', 'Please select at least one task to complete')
        return
    
    indices_to_remove = sorted(list(checked_indices), reverse=True)
    for i in indices_to_remove:
        tasks.pop(i)
        
    num_completed = len(indices_to_remove)
    time_added_seconds = commands.TIME_PER_TASK_SECONDS * num_completed
    time_added_minutes = time_added_seconds // 60 
    commands.timer_seconds += time_added_seconds
    
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox, tasks)
    commands.update_timer_label(timer_label)
    
    messagebox.showinfo('Complete Task', f"Marked {num_completed} task(s) as complete. +{time_added_minutes} minute(s) to timer")

def clear_tasks(tasks_listbox, tasks):
    if not tasks:
        messagebox.showinfo('Clear Tasks', 'The task list is already empty.')
        return
        
    if messagebox.askyesno('Clear All Tasks', 'Are you sure you want to clear ALL tasks?'):
        tasks = []
        commands._write_tasks(tasks)
        populate_tasks_listbox(tasks_listbox)
        messagebox.showinfo('Clear Tasks', 'All tasks have been cleared.')