import json, jingle
from typing import List
from tkinter import messagebox

DATA_FILE = 'data.json'
TIME_FILE = 'time.json'
HISTORY_FILE = 'history.json'
TIMERSECONDS = 'timerseconds.json'
tasks: List[str] = []
timer_seconds = 0
timeLimit = 0

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
        print(f"CONSOLE: Failed to save tasks: {e}")

# TO READ HISTORY FILE
def _read_history() -> List[str]:
    try:
        with open(HISTORY_FILE, 'r') as f: # history.json will be ripped out.
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
    except FileNotFoundError: # If history.json isn't there, we make a new one.
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)
        except Exception:
            pass
        return []
    except Exception:
        return []

def _write_history(history_list: List[str]): # We add a new task to the data.json file.
    try:
        with open(HISTORY_FILE, 'w') as f: # data.json will be ripped out again.
            json.dump(history_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"CONSOLE: Failed to save history file: {e}")
# TO READ HISTORY FILE

# TO READ TIME FILE
def load_time_thru_json_file(): # We make it so that the time.json file is running
    global timeLimit
    try:
        with open(TIME_FILE, 'r') as f: # Program checks if the file is there, so that whatever configuration user has for the timer set can push through
            raw = json.load(f)
            timeLimit = raw
        print(f"CONSOLE: TIME FILE found, now changing.")
    except FileNotFoundError: # Happens when there's no file, so program has to create for user to modify in the meantime. Default is set to 2 minutes
        with open(TIME_FILE, 'w') as f:
            json.dump(120, f)
            
        with open(TIME_FILE, 'r') as f: # Runs it like normal.
            raw = json.load(f)
            timeLimit = raw
        
        print(f"CONSOLE: TIME FILE not found, making file now.")

def change_time_thru_json_file(seconds): # Deliberately tampers the file to accompany the amount of seconds it is loading.
        global timeLimit

        with open(TIME_FILE, 'w') as f:
            json.dump(seconds*60, f)

        with open(TIME_FILE, 'r') as f:
            raw = json.load(f)
            timeLimit = raw
        
        print(f"CONSOLE: Changed time limit.")
# TO READ TIME FILE

# TO READ TIMER SECONDS
def load_time_seconds(): # We make it so that the timerseconds.json file is running
    global timer_seconds
    try:
        with open(TIMERSECONDS, 'r') as f: # Program checks if the file is there, so that whatever configuration user has for the timer set can push through
            raw = json.load(f)
            timer_seconds = raw
        print(f"CONSOLE: TIMERSECONDS found, now changing.")
    except FileNotFoundError: # Happens when there's no file, so program has to create for user to modify in the meantime. Default is set to 2 minutes
        with open(TIMERSECONDS, 'w') as f:
            json.dump(0, f)
            
        with open(TIMERSECONDS, 'r') as f: # Runs it like normal.
            raw = json.load(f)
            timer_seconds = raw

        print(f"CONSOLE: TIMERSOUNDS FILE not found, making file now.")

def reset_timer_seconds(): # Deliberately tampers the file to accompany the amount of seconds it is loading.
        global timer_seconds

        with open(TIMERSECONDS, 'w') as f:
            json.dump(0, f)

        with open(TIMERSECONDS, 'r') as f:
            raw = json.load(f)
            timer_seconds = raw

def add_timer_seconds():
    global timer_seconds
    
    with open(TIMERSECONDS, 'w') as f:
        json.dump(timer_seconds, f)
# TO READ TIMER SECONDS

def format_time(total_seconds: int) -> str:
    hours = total_seconds // 3600 # We turn the total_seconds into hours
    remaining_seconds = total_seconds % 3600 # We give the remaining seconds from the hours made to the seconds
    minutes = remaining_seconds // 60 # We turn these into minutes
    seconds = remaining_seconds % 60 # We see if there are any more left for them to add
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" # We then finish the process by returning the value into a format of hours:minutes:seconds

def update_timer_label(timer_label): # This is to accomodate the fact that the timer is being updated for the amount of time alloted for the user.
    global timer_seconds
    add_timer_seconds()
    load_time_seconds()
    time_str = format_time(timer_seconds)
    timer_label.config(text=f'Time Total: {time_str}')

def reset_timer(timer_label):
    global timer_seconds
    reset_timer_seconds()
    time_str = format_time(timer_seconds)
    timer_label.config(text=f'Time Total: {time_str}')
    messagebox.showinfo("Reset Timer", "Timer has reset.")

def run_countdown(seconds_left, timer_label, buttons, app): # It runs the countdown.
    global timer_seconds, countdown_job
    
    time_str = format_time(seconds_left)
    timer_label.config(text=f'Time left: {time_str}')  # For every second, this updates the label.
    timer_seconds = seconds_left
    add_timer_seconds()
    
    if seconds_left <= 0: # Once the timer is finished, they show this notification to the user.
        jingle.playTune()
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
    messagebox.showinfo("Info", "This is made by KDTal1, an ambitious project.")
