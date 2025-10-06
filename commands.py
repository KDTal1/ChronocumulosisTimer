import json
from typing import List

DATA_FILE = 'data.json'
tasks: List[str] = []
timer_seconds = 0

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
