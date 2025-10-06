import json, mainProcess
from typing import List
from tkinter import messagebox

DATA_FILE = 'data.json'
tasks: List[str] = []
timer_seconds = 0
TIME_PER_TASK_SECONDS = 120

def _read_tasks() -> List[str]:
    try:
        with open(DATA_FILE, 'r') as f: # data.json will be ripped out.
            raw = json.load(f) # Everything in the file will be placed here.
            if isinstance(raw, list):
                result = [] # We make a new list for the tasks.
                for item in raw:
                    if isinstance(item, str):
                        result.append(item) # We add them to another list.
                    elif isinstance(item, dict):
                        result.append(item.get('text', ''))
                    else:
                        result.append(str(item))
                return result
            return []
    except FileNotFoundError: # If data.json isn't there, we make a new one.
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)
        except Exception:
            pass
        return []
    except Exception:
        return []

def _write_tasks(tasks_list: List[str]): # We add a new task to the data.json file.
    try:
        with open(DATA_FILE, 'w') as f: # data.json will be ripped out again.
            json.dump(tasks_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save tasks: {e}")

def format_time(total_seconds: int) -> str:
    hours = total_seconds // 3600 # We turn the total_seconds into hours
    remaining_seconds = total_seconds % 3600 # We give the remaining seconds from the hours made to the seconds
    minutes = remaining_seconds // 60 # We turn these into minutes
    seconds = remaining_seconds % 60 # We see if there are any more left for them to add
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" # We then finish the process by returning the value into a format of hours:minutes:seconds

def update_timer_label(timer_label): # This is to accomodate the fact that the timer is being updated for the amount of time alloted for the user.
    global timer_seconds
    time_str = format_time(timer_seconds)
    timer_label.config(text=f'Time Total: {time_str}')

def run_countdown(seconds_left, timer_label, buttons, app): # It runs the countdown.
    global timer_seconds, countdown_job
    
    time_str = format_time(seconds_left)
    timer_label.config(text=f'Time left: {time_str}')  # For every second, this updates the label.
    
    if seconds_left <= 0: # Once the timer is finished, they show this notification to the user.
        messagebox.showinfo('Timer', 'Timer finished. Returning to menu.')
        timer_seconds = 0
        update_timer_label(timer_label)

        for btn in buttons.values():
            btn.config(state='normal')
        return
    
    countdown_job = app.after(1000, lambda: run_countdown(seconds_left - 1, timer_label, buttons, app))

def start_timer(app, timer_label, buttons): # We force the program to start the timer, so the user can take a break.
    global timer_seconds
    
    time_str = format_time(timer_seconds)
    
    if timer_seconds <= 0:
        messagebox.showinfo('Start Timer', "Your timer is 00:00:00. Complete tasks to add time.") # We make sure if the timer actually has amount of minutes
        return
    
    if not messagebox.askyesno('Start Timer', f'Start timer for {time_str}?'): # Though, we ask the user first.
        return
    
    for btn in buttons.values():
        btn.config(state='disabled') # To ensure every button isn't spammed by the user, 
        
    run_countdown(timer_seconds, timer_label, buttons, app)

def about():
    messagebox.showinfo("Info", "This is made by KdTal1, an ambitious project.")
