"Accumulation Timer 1.2"

'''
Version 1.2

Moved different functions to mainProcess.py, and commands.py
Added comments to mainProcess.py and commands.py

egg.

'''

from tkinter import *
import commands, mainProcess

countdown_job = None
tasks = commands._read_tasks()

app = Tk()
app.title('Accumulation Timer - made by KDTal1')
app.geometry('615x350')
app.resizable(False, False)

tasks_frame = Frame(app, bd=2, relief=GROOVE)
tasks_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 4), sticky='nsew')
tasks_frame.grid_rowconfigure(0, weight=1)
tasks_frame.grid_columnconfigure(0, weight=1)

tasks_listbox = Listbox(tasks_frame, selectmode=EXTENDED, height=10)
tasks_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

scrollbar = Scrollbar(tasks_frame, orient=VERTICAL, command=tasks_listbox.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
tasks_listbox.config(yscrollcommand=scrollbar.set)

mainProcess.populate_tasks_listbox(tasks_listbox, tasks)

controls_frame = Frame(app)
controls_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=4, sticky='ew')

timer_label = Label(app, font=('Arial', 14, 'bold'))
commands.update_timer_label(timer_label) 
timer_label.grid(row=2, column=0, columnspan=4, padx=10, pady=8, sticky='n')

add_btn = Button(controls_frame, text='Add Task', width=14, command=lambda: mainProcess.add_task(app, tasks_listbox, tasks))
complete_btn = Button(controls_frame, text='Mark Complete', width=14, command=lambda: mainProcess.complete_task(tasks_listbox, timer_label, tasks))
start_btn = Button(controls_frame, text='Start Timer', width=14, command=lambda: commands.start_timer(app, timer_label, buttons))
clear_btn = Button(controls_frame, text='Clear All', width=14, command=lambda: mainProcess.clear_tasks(tasks_listbox, tasks))
about_btn = Button(controls_frame, text='About', width=14, command=commands.about)

buttons = {
    'add': add_btn,
    'complete': complete_btn,
    'start': start_btn,
    'clear': clear_btn
}

for btnPack, colNum in [
    (add_btn, 0),
    (complete_btn, 1),
    (start_btn, 2),
    (clear_btn, 3),
    (about_btn, 4)
]:
    btnPack.grid(row=0, column=colNum, padx=5, pady=4, sticky='n')

app.mainloop()