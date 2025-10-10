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

def change_time_json(app, labelTaskMin):
    seconds = simpledialog.askinteger('Change Time', "Switch your minutes from 1-30:", parent=app) # User can choose how many minutes they want to gain from every task completion.
    if not seconds:
        return
    
    if seconds > 30:
        messagebox.showwarning("Error", "Sorry, not allowing that.\n\nYou are only allowed 1-30 minutes for each task.") # If user eats off more than they can chew.
        return
    
    commands.change_time_thru_json_file(seconds)
    update_limit_tasks(labelTaskMin)

def remove_tasks(tasks_listbox, tasks): # mini version of the complete tasks
    checked_indices = tasks_listbox.curselection()
    if not checked_indices:
        messagebox.showinfo("Remove Task", "PLease select at least one task to remove.")
        return
    
    indices_to_remove = sorted(list(checked_indices), reverse=True)
    for i in indices_to_remove:
        tasks.pop(i)
        commands._write_tasks(tasks)
        populate_tasks_listbox(tasks_listbox, tasks)

def complete_task(tasks_listbox, timer_label, tasks, history, app):
    checked_indices = tasks_listbox.curselection() # User can select how many tasks they completed.
    if not checked_indices:
        messagebox.showinfo('Complete Task', 'Please select at least one task to complete') # User may click the button, but if they don't have any tasks, this will show up.
        return
    
    name = simpledialog.askstring('Complete Task', 'Who finished the task?:', parent=app) # User wants to add task, program will ask user what the task is.
    if not name or not name.strip():
        return

    
    indices_to_remove = sorted(list(checked_indices), reverse=True)
    for i in indices_to_remove:
        history.append(f"Task: {tasks[i]}, finished by {name}, added {commands.timeLimit // 60} minutes.")
        commands._write_history(history)

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

def update_limit_tasks(labelTaskMin): # This is to accomodate the fact that the timer is being updated for the amount of time alloted for the user.
    labelTaskMin.config(text=f'Task = {commands.timeLimit // 60} mins')

def clear_tasks(tasks_listbox, tasks): # User doesn't want the tasks, so we're shoving it in the trash can.
    if not tasks: # This happens if tasks are empty
        messagebox.showinfo('Clear All', 'The list is already empty.')
        return
        
    if messagebox.askyesno('Clear All', 'Are you sure you want to clear everything?'): # We give the user an ultimatum first, if they are merciful
        tasks.clear()
        commands._write_tasks(tasks)
        populate_tasks_listbox(tasks_listbox, tasks)
        messagebox.showinfo('Clear Tasks', 'All tasks have been cleared.')

def clear_history(history_listbox, history): # User doesn't want the tasks, so we're shoving it in the trash can.
    if not history: # This happens if tasks are empty
        messagebox.showinfo('Clear All', 'The list is already empty.')
        return
        
    if messagebox.askyesno('Clear All', 'Are you sure you want to clear everything?'): # We give the user an ultimatum first, if they are merciful
        history.clear()
        commands._write_history(history)
        populate_tasks_listbox(history_listbox, history)
        messagebox.showinfo('Clear Tasks', 'All events of history have been cleared.')