import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import *
import json

import commands

countdown_job = None
TIME_PER_TASK_SECONDS = 120

def populate_tasks_listbox(tasks_listbox):
    global tasks
    tasks_listbox.delete(0, tk.END)
    for i, t in enumerate(tasks, start=1):
        tasks_listbox.insert(tk.END, f"{i}. {t}")

def add_task(app, tasks_listbox):
    global tasks
    text = simpledialog.askstring('Add Task', 'Task:', parent=app)
    if not text or not text.strip():
        return
    
    tasks.append(text.strip())
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox)

def complete_task(tasks_listbox, timer_label):
    global tasks, timer_seconds
    
    checked_indices = tasks_listbox.curselection()
    
    if not checked_indices:
        messagebox.showinfo('Complete Task', 'Please select at least one task to complete')
        return
    
    indices_to_remove = sorted(list(checked_indices), reverse=True)
    for i in indices_to_remove:
        tasks.pop(i)
        
    num_completed = len(indices_to_remove)
    time_added_seconds = TIME_PER_TASK_SECONDS * num_completed
    time_added_minutes = time_added_seconds // 60 
    timer_seconds += time_added_seconds
    
    commands._write_tasks(tasks)
    populate_tasks_listbox(tasks_listbox)
    commands.update_timer_label(timer_label)
    
    messagebox.showinfo('Complete Task', f"Marked {num_completed} task(s) as complete. +{time_added_minutes} minute(s) to timer")

def clear_tasks(tasks_listbox):
    global tasks
    
    if not tasks:
        messagebox.showinfo('Clear Tasks', 'The task list is already empty.')
        return
        
    if messagebox.askyesno('Clear All Tasks', 'Are you sure you want to clear ALL tasks?'):
        tasks = []
        commands._write_tasks(tasks)
        populate_tasks_listbox(tasks_listbox)
        messagebox.showinfo('Clear Tasks', 'All tasks have been cleared.')

def run_countdown(seconds_left, timer_label, buttons, app):
    global timer_seconds, countdown_job
    
    time_str = commands.format_time(seconds_left)
    timer_label.config(text=f'Time left: {time_str}') 
    
    if seconds_left <= 0:
        messagebox.showinfo('Timer', 'Timer finished. Returning to menu.')
        timer_seconds = 0
        commands.update_timer_label(timer_label)

        for btn in buttons.values():
            btn.config(state='normal')
        return
    
    countdown_job = app.after(1000, lambda: run_countdown(seconds_left - 1, timer_label, buttons, app))

def start_timer(app, timer_label, buttons):
    global timer_seconds
    
    time_str = commands.format_time(timer_seconds)
    
    if timer_seconds <= 0:
        messagebox.showinfo('Start Timer', "Your timer is 00:00:00. Complete tasks to add time.") 
        return
    
    if not messagebox.askyesno('Start Timer', f'Start timer for {time_str}?'):
        return
    
    for btn in buttons.values():
        btn.config(state='disabled')
        
    run_countdown(timer_seconds, timer_label, buttons, app)

tasks = commands._read_tasks()

app = tk.Tk()
app.title('Pomodoro Task Timer')
app.geometry('500x350')
app.resizable(False, False)

tasks_frame = tk.Frame(app, bd=2, relief=tk.GROOVE)
tasks_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 4), sticky='nsew')

tasks_frame.grid_rowconfigure(0, weight=1)
tasks_frame.grid_columnconfigure(0, weight=1)

tasks_listbox = tk.Listbox(tasks_frame, selectmode=tk.EXTENDED, height=10)
tasks_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

scrollbar = tk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=tasks_listbox.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
tasks_listbox.config(yscrollcommand=scrollbar.set)

populate_tasks_listbox(tasks_listbox)

controls_frame = tk.Frame(app)
controls_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=4, sticky='ew')

timer_label = tk.Label(app, font=('Arial', 14, 'bold'))
commands.update_timer_label(timer_label) 
timer_label.grid(row=2, column=0, columnspan=4, padx=10, pady=8, sticky='n')

add_btn = tk.Button(controls_frame, text='Add Task', width=14, command=lambda: add_task(app, tasks_listbox))
complete_btn = tk.Button(controls_frame, text='Mark as Complete', width=14, command=lambda: complete_task(tasks_listbox, timer_label))
start_btn = tk.Button(controls_frame, text='Start Timer', width=14, command=lambda: start_timer(app, timer_label, buttons))
clear_btn = tk.Button(controls_frame, text='Clear All', width=14, command=lambda: clear_tasks(tasks_listbox))

buttons = {
    'add': add_btn,
    'complete': complete_btn,
    'start': start_btn,
    'clear': clear_btn
}

add_btn.grid(row=0, column=0, padx=5, pady=4, sticky='n')
complete_btn.grid(row=0, column=1, padx=5, pady=4, sticky='n')
start_btn.grid(row=0, column=2, padx=5, pady=4, sticky='n')
clear_btn.grid(row=0, column=3, padx=5, pady=4, sticky='n')

app.mainloop()