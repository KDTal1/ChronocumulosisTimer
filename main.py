"Accumulation Timer 1.3"

'''
Version 1.4

- Label to see how many minutes you can gain per task
- Increased change minutes from 5 mins to 15 mins
- You can now pause your timer when you leave.
- Reset timer button
- History log, Complete Tasks now has accountability feature.

egg.

'''

from tkinter import *
from tkinter import font
from turtle import color
import commands, mainProcess

commands.load_time_thru_json_file()
commands.load_time_seconds()
commands.check_time()

def showHistoryLog(history): # Only appears for 10 seconds.
    top = Toplevel()
    top.title("HISTORY LOG OF TASKS")

    labelEgg = Label(top, text="=-=-=-=-=-=-=-=- HISTORY LOG -=-=-=-=-=-=-=-=", font=("Helvetica", 15, "italic"))
    labelEgg.grid(row=0, column=0)
    history_frame = Frame(top, bd=2, relief=GROOVE)
    history_frame.grid(row=1, column=0, columnspan=10, padx=10, pady=(10, 4), sticky='nsew')
    history_frame.grid_rowconfigure(0, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)

    history_listbox = Listbox(history_frame, selectmode=EXTENDED, height=10)
    history_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

    scrollbar2 = Scrollbar(history_frame, orient=VERTICAL, command=history_listbox.yview)
    scrollbar2.grid(row=0, column=1, sticky='ns')
    history_listbox.config(yscrollcommand=scrollbar2.set)
    mainProcess.populate_tasks_listbox(history_listbox, history)
    top.after(10000, lambda: top.destroy())

btnWidth = 12
button_color = "#E67892"
about_color = "#7FCF66"
font_for_btn = ("Helvetica", 12)

countdown_job = None
tasks = commands._read_tasks()
history = commands._read_history()

app = Tk()
app.title('Accumulation To-Do List Timer 1.4')
app.geometry('415x370')
app.resizable(False, False)

# FRAME 1
tasks_frame = Frame(app, bd=2, relief=GROOVE)
tasks_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 4), sticky='nsew')
tasks_frame.grid_rowconfigure(0, weight=1)
tasks_frame.grid_columnconfigure(0, weight=1)

tasks_listbox = Listbox(tasks_frame, selectmode=EXTENDED, height=10)
tasks_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

scrollbar = Scrollbar(tasks_frame, orient=VERTICAL, command=tasks_listbox.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
tasks_listbox.config(yscrollcommand=scrollbar.set)
# FRAME 1

mainProcess.populate_tasks_listbox(tasks_listbox, tasks)

controls_frame = Frame(app)
controls_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=4, sticky='ew')

timer_label = Label(app, font=('Arial', 14, 'bold'))
commands.update_timer_label(timer_label) 
timer_label.grid(row=2, column=0, columnspan=4, padx=10, pady=8, sticky='n')

add_btn = Button(controls_frame, text='Add Task', width=btnWidth, command=lambda: mainProcess.add_task(app, tasks_listbox, tasks), font=font_for_btn, bg=button_color)
complete_btn = Button(controls_frame, text='Mark Complete', width=btnWidth, command=lambda: mainProcess.complete_task(tasks_listbox, timer_label, tasks, history, app), font=font_for_btn, bg=button_color)
start_btn = Button(controls_frame, text='Start Timer', width=btnWidth, command=lambda: commands.start_timer(app, timer_label, buttons), font=font_for_btn, bg=button_color)
clear_btn = Button(controls_frame, text='Clear All', width=btnWidth, command=lambda: mainProcess.clear_tasks(tasks_listbox, tasks), font=font_for_btn, bg=button_color)
about_btn = Button(controls_frame, text='About', width=btnWidth, command=commands.about, font=font_for_btn, bg=about_color)
change_time = Button(controls_frame, text='Change Minutes', width=btnWidth, command=lambda: mainProcess.change_time_json(app), font=font_for_btn, bg=button_color)
history_btn = Button(controls_frame, text="History Log", width=btnWidth, command=lambda: showHistoryLog(history), font=font_for_btn, bg=button_color)
reset_btn = Button(controls_frame, text="Reset Timer", width=btnWidth, command=lambda: commands.reset_timer(timer_label), font=font_for_btn, bg=button_color)

labelTaskMin = Label(controls_frame, font=('Arial', 14, 'bold'))
mainProcess.update_limit_tasks(labelTaskMin)
labelTaskMin.grid(row=2, column=1, padx=5, pady=4)

buttons = {
    'add': add_btn,
    'complete': complete_btn,
    'start': start_btn,
    'clear': clear_btn,
    'timin': change_time,
    'reset': reset_btn
}

for btnPack, colNum, rowNum in [
    (add_btn, 0, 0),
    (complete_btn, 1, 0),
    (start_btn, 2, 0),
    (clear_btn, 0, 1),
    (about_btn, 1, 1),
    (change_time, 2, 1),
    (history_btn, 0, 2),
    (reset_btn, 2, 2)
]:
    btnPack.grid(row=rowNum, column=colNum, padx=5, pady=4)

app.mainloop()