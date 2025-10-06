import json, mainProcess
from typing import List
from tkinter import messagebox

DATA_FILE = 'data.json'
tasks: List[str] = []
timer_seconds = 0
TIME_PER_TASK_SECONDS = 120

def _read_tasks() -> List[str]:
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            if isinstance(raw, list):
                result = []
                for item in raw:
                    if isinstance(item, str):
                        result.append(item)
                    elif isinstance(item, dict):
                        result.append(item.get('text', ''))
                    else:
                        result.append(str(item))
                return result
            return []
    except FileNotFoundError:
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        except Exception:
            pass
        return []
    except Exception:
        return []

def _write_tasks(tasks_list: List[str]):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save tasks: {e}")

def format_time(total_seconds: int) -> str:
    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def update_timer_label(timer_label):
    global timer_seconds
    time_str = format_time(timer_seconds)
    timer_label.config(text=f'Time Total: {time_str}')

def run_countdown(seconds_left, timer_label, buttons, app):
    global timer_seconds, countdown_job
    
    time_str = format_time(seconds_left)
    timer_label.config(text=f'Time left: {time_str}') 
    
    if seconds_left <= 0:
        messagebox.showinfo('Timer', 'Timer finished. Returning to menu.')
        timer_seconds = 0
        update_timer_label(timer_label)

        for btn in buttons.values():
            btn.config(state='normal')
        return
    
    countdown_job = app.after(1000, lambda: run_countdown(seconds_left - 1, timer_label, buttons, app))

def start_timer(app, timer_label, buttons):
    global timer_seconds
    
    time_str = format_time(timer_seconds)
    
    if timer_seconds <= 0:
        messagebox.showinfo('Start Timer', "Your timer is 00:00:00. Complete tasks to add time.") 
        return
    
    if not messagebox.askyesno('Start Timer', f'Start timer for {time_str}?'):
        return
    
    for btn in buttons.values():
        btn.config(state='disabled')
        
    run_countdown(timer_seconds, timer_label, buttons, app)
