"Chronocumulosis Timer - KDTal1"

'''
v1.0 - The Initial Loadout.

Developer's Notes:

I tried my best polishing everything from here, making sure that everything is all accounted for before actual release.
This is the main source code of the software. There are three files that run with it.

guiFunctions - They are all the functions that are used to modify the GUI thru event changes, updates within the timer, accounting tasks, and communicating with mainFunctions.
mainFunctions - They are the functions that run the most processes in the application.
jingle - What do you expect? It's the jingle file.

It runs with the following outside dependencies:
- PyGame
- Numpy

'''

from tkinter import *
from tkinter import font
import mainFunctions, guiFunctions

mainFunctions.load_time_thru_json_file()
mainFunctions.load_time_seconds()
mainFunctions.jsonTurned_variable()

def showHistoryLog(history): # Only appears for 10 seconds.
    top = Toplevel()
    top.title("HISTORY LOG - Chronocumulosis")
    top.configure(bg=backgroundCol)
    top.resizable(False, False)

    labelEgg = Label(top, text="                            --- HISTORY LOG ---                            ", font=("Helvetica", 15, "italic"), bg=backgroundCol, fg='white')
    labelEgg.grid(row=0, column=0)

    historyRemove = Button(top, text="Erase History", 
                           command=lambda: guiFunctions.clear_history(history_listbox, history), 
                           font=font_for_btn, bg=main_color, fg='white')
    historyRemove.grid(row=2, column=0, sticky='nsew', padx=4, pady=4)

    history_frame = Frame(top, bd=2, relief=GROOVE, bg=backgroundCol)
    history_frame.grid(row=1, column=0, columnspan=10, padx=10, pady=(10, 4), sticky='nsew')
    history_frame.grid_rowconfigure(0, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)

    history_listbox = Listbox(history_frame, selectmode=EXTENDED, height=10, bg=main_color, fg='white')
    history_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

    scrollbar2 = Scrollbar(history_frame, orient=VERTICAL, command=history_listbox.yview)
    scrollbar2.grid(row=0, column=1, sticky='ns')
    history_listbox.config(yscrollcommand=scrollbar2.set)

    guiFunctions.populate_tasks_listbox(history_listbox, history)
    top.after(10000, lambda: top.destroy())

btnWidth = 12
main_color = "#4F4E79"
backgroundCol = "#1C1B26"
font_for_btn = ("Consolas", 12)

countdown_job = None
tasks = mainFunctions._read_tasks()
history = mainFunctions._read_history()

app = Tk()
app.title('Chronocumulosis - Accumulation Timer')
app.geometry('405x380')
app.resizable(False, False)
app.configure(bg=backgroundCol)

# FRAME 1
tasks_frame = Frame(app, bd=2, relief=GROOVE, bg=backgroundCol)
tasks_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 4), sticky='nsew')
tasks_frame.grid_rowconfigure(0, weight=1)
tasks_frame.grid_columnconfigure(0, weight=1)

tasks_listbox = Listbox(tasks_frame, selectmode=EXTENDED, height=10, bg=main_color, fg='white')
tasks_listbox.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

scrollbar = Scrollbar(tasks_frame, orient=VERTICAL, command=tasks_listbox.yview, bg=main_color)
scrollbar.grid(row=0, column=1, sticky='ns')
tasks_listbox.config(yscrollcommand=scrollbar.set)
# FRAME 1

guiFunctions.populate_tasks_listbox(tasks_listbox, tasks)

controls_frame = Frame(app, bg=backgroundCol)
controls_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=4, sticky='ew')
labelsFrame = Frame(app, bg=backgroundCol)
labelsFrame.grid(row=2, column=0, columnspan=4, padx=10, pady=8, sticky='n')

timer_label = Label(labelsFrame, font=('Consolas', 14, 'bold'), bg=backgroundCol, fg='white')
mainFunctions.update_timer_label(timer_label) 
timer_label.grid(row=0, column=0, padx=5, pady=5)

labelTaskMin = Label(labelsFrame, font=('Consolas', 14, 'bold'), bg=backgroundCol, fg='white')
guiFunctions.update_limit_tasks(labelTaskMin)
labelTaskMin.grid(row=0, column=1, padx=5, pady=5)


add_btn = Button(controls_frame, text='add', width=btnWidth, 
                 command=lambda: guiFunctions.add_task(app, tasks_listbox, tasks), 
                 font=font_for_btn, bg=main_color, fg='white')

complete_btn = Button(controls_frame, text='complete', width=btnWidth, 
                      command=lambda: guiFunctions.complete_task(tasks_listbox, timer_label, tasks, history, app, mainFunctions.praise_messages), 
                      font=font_for_btn, bg=main_color, fg='white')

start_btn = Button(controls_frame, text='start', width=btnWidth, 
                   command=lambda: mainFunctions.start_timer(app, timer_label, buttons), 
                   font=font_for_btn, bg=main_color, fg='white')

clear_btn = Button(controls_frame, text='clear', width=btnWidth, 
                   command=lambda: guiFunctions.clear_tasks(tasks_listbox, tasks), 
                   font=font_for_btn, bg=main_color, fg='white')

about_btn = Button(controls_frame, text='about', width=btnWidth, 
                   command=mainFunctions.about, 
                   font=font_for_btn, bg=main_color, fg='white')

change_time = Button(controls_frame, text='set time', width=btnWidth, 
                     command=lambda: guiFunctions.change_time_json(app, labelTaskMin), 
                     font=font_for_btn, bg=main_color, fg='white')

history_btn = Button(controls_frame, text="history", width=btnWidth, 
                     command=lambda: showHistoryLog(history), 
                     font=font_for_btn, bg=main_color, fg='white')

remove_btn = Button(controls_frame, text="remove", width=btnWidth, 
                    command=lambda: guiFunctions.remove_tasks(tasks_listbox, tasks), 
                    font=font_for_btn, bg=main_color, fg='white')

reset_btn = Button(controls_frame, text="reset", width=btnWidth, 
                   command=lambda: mainFunctions.reset_timer(timer_label), 
                   font=font_for_btn, bg=main_color, fg='white')

buttons = {
    'add': add_btn,
    'complete': complete_btn,
    'start': start_btn,
    'clear': clear_btn,
    'timin': change_time,
    'reset': reset_btn,
    'remove': remove_btn
}

for btnPack, colNum, rowNum in [
    (add_btn, 0, 0),
    (complete_btn, 1, 0),
    (start_btn, 2, 0),
    (clear_btn, 0, 1),
    (about_btn, 1, 1),
    (change_time, 2, 1),
    (history_btn, 0, 2),
    (remove_btn, 1, 2),
    (reset_btn, 2, 2)
]:
    btnPack.grid(row=rowNum, column=colNum, padx=5, pady=4)

app.mainloop()
