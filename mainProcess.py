from tkinter import simpledialog, messagebox
from tkinter import *
import commands

def populate_tasks_listbox(tasks_listbox, tasks):
    tasks_listbox.delete(0, END)
    for i, t in enumerate(tasks, start=1):
        tasks_listbox.insert(END, f"{i}. {t}")

def add_task(app, tasks_listbox, tasks):
    text = simpledialog.askstring('Add Task', 'Task:', parent=app) # User wants to add task, program will ask user what the task is.
    if not text or not text.strip():
        return
    
    # Whole segment will add the task into the list box.
    tasks.append(text.strip())
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox, tasks)

def change_time_json(app):
    seconds = simpledialog.askinteger('CHange Time', "Switch your minutes from 1-5:", parent=app)
    if not seconds:
        return
    
    if seconds > 5:
        messagebox.showwarning("Error", "Sorry, not allowing that.\n\nYou are only allowed 1-5 minutes for each task.")
        return
    
    commands.change_time_thru_json_file(seconds)
    commands.check_time()

def complete_task(tasks_listbox, timer_label, tasks):
    checked_indices = tasks_listbox.curselection() # User can select how many tasks they completed.
    
    if not checked_indices:
        messagebox.showinfo('Complete Task', 'Please select at least one task to complete') # User may click the button, but if they don't have any tasks, this will show up.
        return
    
    indices_to_remove = sorted(list(checked_indices), reverse=True)
    for i in indices_to_remove:
        tasks.pop(i) # Completed task is done, now you just remove them.
    
    num_completed = len(indices_to_remove) # The amount of tasks that are completed
    time_added_seconds = commands.timeLimit * num_completed # The amount of tasks converted into minutes for the timer (Currently in seconds.)
    time_added_minutes = time_added_seconds // 60 # The seconds became minutes
    commands.timer_seconds += time_added_seconds # The minutes are stored in the timer_seconds, it can be shoved there. Nothing more.
    
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox, tasks)
    commands.update_timer_label(timer_label)
    
    messagebox.showinfo('Complete Task', f"Marked {num_completed} task(s) as complete. +{time_added_minutes} minute(s) to timer")
    # num_completed - The amount of tasks completed by user
    # time_added_minutes - The converted version of time_added_seconds for user to comprehend how many minutes they accumulated.

def clear_tasks(tasks_listbox, tasks): # User doesn't want the tasks, so we're shoving it in the trash can.
    if not tasks: # This happens if tasks are empty
        messagebox.showinfo('Clear Tasks', 'The task list is already empty.')
        return
        
    if messagebox.askyesno('Clear All Tasks', 'Are you sure you want to clear ALL tasks?'): # We give the user an ultimatum first, if they are merciful
        tasks.clear()
        commands._write_tasks(tasks)
        populate_tasks_listbox(tasks_listbox, tasks)
        messagebox.showinfo('Clear Tasks', 'All tasks have been cleared.')