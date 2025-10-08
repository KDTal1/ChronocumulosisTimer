"Accumulation Timer 1.3"

'''
Version 1.3

Decoration, and optimizations.

egg.

'''

from tkinter import *
import commands, mainProcess

commands.load_time_thru_json_file()
commands.check_time()

btnWidth = 12
button_color = "#E67892"
about_color = "#7FCF66"
font_for_btn = ("Helvetica", 12)

countdown_job = None
tasks = commands._read_tasks()

app = Tk()
app.title('Accumulation Timer 1.3 - Made by KDTal1')
app.geometry('405x350')
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

add_btn = Button(controls_frame, text='Add Task', width=btnWidth, command=lambda: mainProcess.add_task(app, tasks_listbox, tasks), font=font_for_btn, bg=button_color)
complete_btn = Button(controls_frame, text='Mark Complete', width=btnWidth, command=lambda: mainProcess.complete_task(tasks_listbox, timer_label, tasks), font=font_for_btn, bg=button_color)
start_btn = Button(controls_frame, text='Start Timer', width=btnWidth, command=lambda: commands.start_timer(app, timer_label, buttons), font=font_for_btn, bg=button_color)
clear_btn = Button(controls_frame, text='Clear All', width=btnWidth, command=lambda: mainProcess.clear_tasks(tasks_listbox, tasks), font=font_for_btn, bg=button_color)
about_btn = Button(controls_frame, text='About', width=btnWidth, command=commands.about, font=font_for_btn, bg=button_color)
change_time = Button(controls_frame, text='Change Minutes', width=btnWidth, command=lambda: mainProcess.change_time_json(app), font=font_for_btn, bg=about_color)

buttons = {
    'add': add_btn,
    'complete': complete_btn,
    'start': start_btn,
    'clear': clear_btn,
    'timin': change_time
}

for btnPack, colNum, rowNum in [
    (add_btn, 0, 0),
    (complete_btn, 1, 0),
    (start_btn, 2, 0),
    (clear_btn, 0, 1),
    (about_btn, 1, 1),
    (change_time, 2, 1)
]:
    btnPack.grid(row=rowNum, column=colNum, padx=5, pady=4)

app.mainloop()