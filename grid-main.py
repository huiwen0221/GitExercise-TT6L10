from tkinter import *
import time
import sqlite3
from datetime import datetime
from tkinter import ttk,colorchooser,PhotoImage, messagebox
import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plyer import notification
import threading
from tkcalendar import Calendar


class MainInterface:
    def __init__(self,root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("1000x700")
        self.root.configure(bg = "IndianRed")

        self.window_icon = PhotoImage(file="pomodoro helper.png")
        self.root.iconphoto(False,self.window_icon)

        pygame.init()
        pygame.mixer.init()
        global counter
        counter=1

        #Defining Grid 
        self.root.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
        self.root.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight = 1, uniform='a')

        # Create database for Pomodoro
        self.conn = sqlite3.connect('pomodorohelper.db')
        self.cursor = self.conn.cursor()

        # Create Table if not exists
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PomodoroSessions (
            SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
            User TEXT NOT NULL,
            Mode TEXT NOT NULL,
            SessionType TEXT NOT NULL,
            Duration INTEGER NOT NULL,
            CompletionTime TEXT NOT NULL
        );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Presets (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TimerDuration INTEGER,
            ShortBreakDuration INTEGER,
            LongBreakDuration INTEGER,
            RepeatCycles INTEGER,
            TimerEndSound TEXT,
            ShortBreakSound TEXT,
            LongBreakSound TEXT,
            BackgroundColor TEXT,
            Volume INTEGER
        );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT NOT NULL,
        due_time TEXT NOT NULL
        );""")



        self.sound_files = {
            "Default Alarm": "Default Timer Alarm.wav",
            "Referee Whistle": "Study Referee Alarm.wav",
            "Chime": "Relax Chime Alarm.wav",
            "Default Short Break": "Default SB.wav",
            "Churchbell": "Study Churchbell SB.wav",
            "Wind Chimes": "Relax WindChimes SB.wav",
            "Default Microwave": "Default Microwave LB.wav",
            "Great Harp": "Study Great Harp LB.wav",
            "Relaxing Harp": "Relax Harp LB.wav"
        }

        self.timer_end_sound = self.sound_files["Default Alarm"]
        self.short_break_sound = self.sound_files["Default Short Break"]
        self.long_break_sound = self.sound_files["Default Microwave"]
        self.background_color="Indianred"

        self.badges = {15: "badge1.png", 30: "badge2.png", 60: "badge3.png"}  # Dictionary of badges and their cumulative time thresholds
        self.collected_badges = []  # List to store collected badges
        self.cumulative_time = 0  # Cumulative time counter
        self.study_frame = None
        self.due_date_selected = False
        self.due_time_selected = False
        self.calendar_tasks = {}
        self.task_widgets = []
        self.task_count = 0
        self.task_count_label=0
#Study Mode variables
        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_shortbreak_duration = 900
        self.study_longbreak_duration = 1500
        self.is_music_playing = False
        self.volume = 50
        self.study_type = "study_timer"
        self.study_cycle_count = 0


        self.selected_date = None
        self.selected_time = None
        self.task_widgets = []
        self.task_count = 0
        self.calendar_tasks = {}
        self.due_date_selected = False
        self.due_time_selected = False
#Relax Mode variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_shortbreak_duration = 1200
        self.relax_longbreak_duration = 1800

        self.relax_type = "relax_timer"
        self.relax_cycle_count = 0

        self.current_plot = None

        def user_data():
            window = Toplevel(root)
            window.title("Statistics")
            window.geometry("800x600")

            def plot_statistics(window, data, x_label, y_label):
                # Clear the current plot if exist

                fig, ax = plt.subplots(figsize=(10, 6))
                # Break duration
                ax.bar(data.index, data['Break Duration'], label='Break', color='blue', alpha=0.5)
                # Timer duration
                ax.bar(data.index, data['Timer Duration'], bottom=data['Break Duration'], label='Timer', color='orange', alpha=0.5)
                ax.set_title('Pomodoro Statistics')
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.legend()

                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().grid(row=1, column=0, columnspan=10, rowspan=9, sticky="nsew")
                self.current_plot = canvas

            def show_weekly():
                self.cursor.execute('''
                    SELECT strftime('%w', CompletionTime) AS Weekday, 
                        SUM(CASE WHEN SessionType = 'Short Break' OR SessionType = 'Long Break' THEN Duration ELSE 0 END) AS BreakDuration, 
                        SUM(CASE WHEN SessionType = 'Timer' THEN Duration ELSE 0 END) AS TimerDuration 
                    FROM PomodoroSessions 
                    GROUP BY Weekday
                ''')
                weekly_data = self.cursor.fetchall()
                weekdays_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                weekly = pd.DataFrame(weekly_data, columns=['Weekday', 'Break Duration', 'Timer Duration'])
                weekly['Weekday'] = weekly['Weekday'].astype(int).apply(lambda x: weekdays_order[x])
                weekly.set_index('Weekday', inplace=True)
                weekly['Break Duration'] /= 60
                weekly['Timer Duration'] /= 60
                plot_statistics(window, data=weekly, x_label='Weekday', y_label='Duration (hours)')

            def show_monthly():
                self.cursor.execute('''
                    SELECT strftime('%Y-%m', CompletionTime) AS MonthStart, 
                        SUM(CASE WHEN SessionType = 'Short Break' OR SessionType = 'Long Break' THEN Duration ELSE 0 END) AS BreakDuration, 
                        SUM(CASE WHEN SessionType = 'Timer' THEN Duration ELSE 0 END) AS TimerDuration 
                    FROM PomodoroSessions 
                    GROUP BY MonthStart
                ''')
                monthly_data = self.cursor.fetchall()
                monthly = pd.DataFrame(monthly_data, columns=['MonthStart', 'Break Duration', 'Timer Duration'])
                monthly.set_index('MonthStart', inplace=True)
                monthly['Break Duration'] /= 60
                monthly['Timer Duration'] /= 60
                plot_statistics(window, data=monthly, x_label='Month Start', y_label='Duration (hours)')

            # Buttons for weekly and monthly data
            weekly_button = Button(window, text="Show Weekly", command=show_weekly)
            weekly_button.grid(row=0, column=5, padx=10, pady=10)
            monthly_button = Button(window, text="Show Monthly", command=show_monthly)
            monthly_button.grid(row=0, column=6, padx=10, pady=10)


        def studylist_user():
            study = Toplevel(root)
            study.title("Study List")
            study.geometry("1300x600")
            study.configure(bg="Indian Red")
            study.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')
            study.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')
            self.study_frame = Frame(study, bg="white")
            self.study_frame.grid(row=2, column=0, columnspan=10, rowspan=9, padx=20, pady=10, sticky="nsew")
            self.task_count_label = Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 10), bg="white")
            self.task_count_label.grid(row=1, column=0, padx=20, sticky="w")

            def confirm_time(hour, minute, top):
                self.selected_time = f"{hour}:{minute}"
                self.due_time_selected = True
                top.destroy()
                self.due_time_button.config(state=DISABLED)  # Disable the due time button after selection

            def add_completed_column():
                cursor = self.conn.cursor()
                cursor.execute("PRAGMA table_info(tasks)")
                columns = [column[1] for column in cursor.fetchall()]
                if 'completed' not in columns:
                    with self.conn:
                        self.conn.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")
                        self.conn.commit()
            
            def add_task():
                new_task = self.new_task_entry.get()
                if new_task and self.selected_date and self.selected_time:
                    add_task_to_study_list(new_task, self.selected_date, self.selected_time)
                    self.new_task_entry.delete(0, "end")
                    self.selected_date = None
                    self.selected_time = None

                    # Re-enable the due date and due time buttons
                    self.due_date_button.config(state=NORMAL)
                    self.due_time_button.config(state=NORMAL)
                else:
                    messagebox.showwarning("Warning", "Please enter a task, select its due date, and set the time.")


            def add_task_to_study_list(new_task, due_date, due_time, from_db=False):
                task_row = self.task_count + 2

                # Checkbutton for new task
                task_checkbutton = Checkbutton(self.study_frame, text=new_task, font=("Times New Roman", 20), bg="white")
                task_checkbutton.grid(row=task_row, column=0, sticky="w", pady=(5, 0))

                task_checkbutton.var = BooleanVar()
                task_checkbutton.config(variable=task_checkbutton.var, command=lambda cb=task_checkbutton, tt=new_task, dt=due_date, tm=due_time: mark_completed(cb, tt, dt, tm))

                # Frame to hold due date and due time
                due_info_frame = Frame(self.study_frame, bg="light yellow")
                due_info_frame.grid(row=task_row, column=1, sticky="ew", padx=20, pady=(5, 0), columnspan=2)

                # Frame to hold both due date and due time in the same box
                due_date_time_frame = Frame(due_info_frame, bd=1, relief=SOLID, bg="light yellow")
                due_date_time_frame.pack(side="left", padx=5, fill=X, expand=True)

                # Due date label
                due_date_label = Label(due_date_time_frame, text=f"Due Date: {due_date}", font=("Times New Roman", 10), bg="light yellow")
                due_date_label.pack(padx=5, pady=2)

                # Due time label
                due_time_label = Label(due_date_time_frame, text=f"Due Time: {due_time}", font=("Times New Roman", 10), bg="light yellow")
                due_time_label.pack(padx=5, pady=2)

                self.task_widgets.append((task_checkbutton, due_info_frame))

                self.task_count += 1
                self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

                if due_date not in self.calendar_tasks:
                    self.calendar_tasks[due_date] = []
                self.calendar_tasks[due_date].append((new_task, due_time))

                if not from_db:
                    self.save_task(new_task, due_date, due_time)

                schedule_notification(new_task, due_date, due_time)
                
                # Re-enable the due date and due time buttons
                self.due_date_button.config(state=NORMAL)
                self.due_time_button.config(state=NORMAL)

            def update_task_count_label():
                self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

            def create_table():
                with self.conn:
                    self.conn.execute("""
                        CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        due_date TEXT NOT NULL,
                        due_time TEXT NOT NULL
                    );""")

            def load_tasks():
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT task, due_date, due_time FROM tasks")
                    tasks = cursor.fetchall()
                    for task_info in tasks:
                        task, due_date, due_time = task_info
                        # Add task to your application logic here
                        print(f"Loaded task: {task} due on {due_date} at {due_time}")
                        add_task_to_study_list(task, due_date, due_time, from_db=True)  # Call add_task_to_study_list with from_db=True
                except Exception as e:
                    print(f"Error loading tasks: {e}")

            def select_due_date():               
                top = Toplevel()
                cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', font=('Times New Roman', 10), bg="light yellow")
                cal.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

                confirm_button = Button(top, text="Confirm", command=lambda: confirm_due_date(cal, top), font=("Times New Roman", 10), bg="light yellow")
                confirm_button.grid(row=1, column=0, pady=5, sticky="s")

                # Configure row and column weights for proper resizing
                top.grid_rowconfigure(0, weight=1)
                top.grid_columnconfigure(0, weight=1)

            def confirm_due_date(cal, top):
                self.selected_date = cal.get_date()
                self.due_date_selected = True
                top.destroy()

            def select_time():
                                
                top = Toplevel()
                top.title("Select Time")
                top.geometry("200x300")

                hour_label = Label(top, text="Hour (0-23):", font=("Times New Roman", 10))
                hour_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
                hour_combobox = ttk.Combobox(top, font=("Times New Roman", 10), values=[f"{i:02d}" for i in range(24)])
                hour_combobox.grid(row=1, column=0, padx=20, pady=10, sticky="w")
                hour_combobox.current(0)  # Set default value to 00

                minute_label = Label(top, text="Minute (0-59):", font=("Times New Roman", 10))
                minute_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
                minute_combobox = ttk.Combobox(top, font=("Times New Roman", 10), values=[f"{i:02d}" for i in range(60)])
                minute_combobox.grid(row=3, column=0, padx=20, pady=10, sticky="w")
                minute_combobox.current(0)  # Set default value to 00

                confirm_button = Button(top, text="Confirm", font=("Times New Roman", 10),
                                                    command=lambda: confirm_time(hour_combobox.get(), minute_combobox.get(), top))
                confirm_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")


            def delete_all_tasks():
                            for task_widget in self.task_widgets:
                                task_widget[0].destroy()
                                task_widget[1].destroy()

                            self.task_widgets.clear()
                            self.task_count = 0
                            self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

                            # Clear tasks from the database
                            with self.conn:
                                self.conn.execute("DELETE FROM tasks")
                                self.conn.commit()

            def delete_selected_tasks():
                            selected_tasks = [task_widget for task_widget in self.task_widgets if task_widget[0].var.get()]
                            
                            # Collect information to delete from the database
                            tasks_to_delete = []
                            for task_widget in selected_tasks:
                                task_text = task_widget[0].cget("text")
                                
                                # Get the children of due_info_frame's child frame, which are due_date_label and due_time_label
                                due_info_frame = task_widget[1]
                                due_date_time_frame = due_info_frame.winfo_children()[0]  # This should be the frame containing the labels
                                due_date_label = due_date_time_frame.winfo_children()[0]  # First child is the due date label
                                due_time_label = due_date_time_frame.winfo_children()[1]  # Second child is the due time label
                                
                                due_date = due_date_label.cget("text").replace("Due Date: ", "")
                                due_time = due_time_label.cget("text").replace("Due Time: ", "")
                                
                                tasks_to_delete.append((task_text, due_date, due_time))

                            # Destroy the widgets
                            for task_widget in selected_tasks:
                                task_widget[0].destroy()
                                task_widget[1].destroy()
                                self.task_widgets.remove(task_widget)
                                self.task_count -= 1

                            # Update task count label
                            self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

                            # Delete selected tasks from the database
                            with self.conn:
                                for task_text, due_date, due_time in tasks_to_delete:
                                    self.conn.execute("DELETE FROM tasks WHERE task = ? AND due_date = ? AND due_time = ?", (task_text, due_date, due_time))
                                self.conn.commit()

                            # Remove from calendar_tasks if present
                            for task_text, due_date, due_time in tasks_to_delete:
                                if due_date in self.calendar_tasks:
                                    self.calendar_tasks[due_date] = [(task, t) for task, t in self.calendar_tasks[due_date] if task != task_text]
                                    if not self.calendar_tasks[due_date]:
                                        del self.calendar_tasks[due_date]

                                # Delete selected tasks from the database
                                with self.conn:
                                    for task_text, due_date, due_time in tasks_to_delete:
                                        self.conn.execute("DELETE FROM tasks WHERE task = ? AND due_date = ? AND due_time = ?", (task_text, due_date, due_time))
                                    self.conn.commit()

                                # Remove from calendar_tasks if present
                                for task_text, due_date, due_time in tasks_to_delete:
                                    if due_date in self.calendar_tasks:
                                        self.calendar_tasks[due_date] = [(task, t) for task, t in self.calendar_tasks[due_date] if task != task_text]
                                        if not self.calendar_tasks[due_date]:
                                            del self.calendar_tasks[due_date]


            def mark_completed(task_checkbutton, task_text, due_date, due_time):
                            if task_checkbutton.var.get():
                                task_checkbutton.config(fg="grey")
                            else:
                                task_checkbutton.config(fg="black")

                            # Update the task's completion status in the database (if necessary)
                            with self.conn:
                                self.conn.execute("UPDATE tasks SET completed = ? WHERE task = ? AND due_date = ? AND due_time = ?",
                                                (task_checkbutton.var.get(), task_text, due_date, due_time))
                                self.conn.commit()

            def open_calendar():
                # Close previous calendar window if exists
                if hasattr(self, "calendar_window"):
                    self.calendar_window.destroy()

                # Create a top-level window for the calendar
                self.calendar_window = Toplevel(root)
                self.calendar_window.title("Calendar")
                self.calendar_window.geometry("600x400")  # Set the size of the Toplevel window

                # Create the calendar widget
                self.calendar = Calendar(self.calendar_window, font="Arial 14", selectmode='day')
                self.calendar.grid(row=0, column=0, sticky="nsew")

                # Bind a function to handle date selection on the calendar
                self.calendar.bind("<<CalendarSelected>>", lambda event: display_calendar_tasks(event, self.calendar, self.calendar_window))

                # Frame to display the tasks for the selected date
                self.task_frame = Frame(self.calendar_window, bg="light yellow", width=200)  # Fixed width for smaller size
                self.task_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

                # Configure grid weights for resizing
                self.calendar_window.grid_columnconfigure(0, weight=1)
                self.calendar_window.grid_columnconfigure(1, weight=1)
                self.calendar_window.grid_rowconfigure(0, weight=1)

                # Update the calendar frame to reflect current tasks
                update_calendar_frame()


            def display_calendar_tasks(event, calendar, calendar_window):
                    # Get the selected date from the calendar
                    # Get the selected date from the calendar
                    selected_date = datetime.strptime(calendar.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")

                    # Get tasks associated with the selected date
                    tasks = self.calendar_tasks.get(selected_date, [])

                    # Clear existing tasks
                    for widget in self.task_frame.winfo_children():
                        widget.destroy()

                    # Create a label to show the selected date
                    date_label = Label(self.task_frame, text=f"Tasks for {selected_date}", font=("Arial", 14), bg="light yellow")
                    date_label.grid(pady=10)

                    # Display tasks associated with the selected date
                    for task, due_time in tasks:  # Each task is a tuple (task, due_time)
                        task_label = Label(self.task_frame, text=f"{task} at {due_time}", font=("Arial", 12), bg="light yellow")
                        task_label.grid(pady=5)


            def update_calendar_frame():
                    # Get the currently selected date from the calendar
                    if hasattr(self, "calendar"):
                        selected_date = datetime.strptime(self.calendar.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")

                        # Get tasks associated with the selected date
                        tasks = self.calendar_tasks.get(selected_date, [])

                        # Clear existing tasks
                        for widget in self.task_frame.winfo_children():
                            widget.destroy()

            def schedule_notification(task, due_date, due_time):
                        due_datetime_str = f"{due_date} {due_time}"
                        due_datetime = datetime.strptime(due_datetime_str, "%Y-%m-%d %H:%M")
                        delay = (due_datetime - datetime.now()).total_seconds()

                        if delay > 0:
                            threading.Timer(delay, show_notification, args=(task,)).start()
                            print(f"Scheduled notification for task '{task}' at {due_datetime_str}")

            def show_notification(task):
                notification.notify(
                            title="Task Due",
                            message=f"The task '{task}' is due now!",
                            timeout=10
                        )
            def load_tasks():
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT task, due_date, due_time FROM tasks")
                    tasks = cursor.fetchall()
                    for task_info in tasks:
                        task, due_date, due_time = task_info
                        # Add task to your application logic here
                        print(f"Loaded task: {task} due on {due_date} at {due_time}")
                        add_task_to_study_list(task, due_date, due_time, from_db=True)  # Call add_task_to_study_list with from_db=True
                except Exception as e:
                    print(f"Error loading tasks: {e}")

                # Initialize the SQLite database
            self.conn = sqlite3.connect("tasks.db")
            create_table()
            add_completed_column() 
            load_tasks()
            update_task_count_label()

            
            self.calendar_button = Button(study, text="Calendar", command=open_calendar, bg="white")
            self.calendar_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            self.title_label = Label(study, text="Study List", font=("Cooper Black", 45), bg="Indian Red")
            self.title_label.grid(row=0, column=2, columnspan=5, sticky="nsew")

            self.new_task_entry = Entry(study, font=("Times New Roman", 17), width=20)
            self.new_task_entry.grid(row=1, column=0, columnspan=7, sticky="ew", padx=(10, 0))

            self.due_date_button = Button(study, text="Select Due Date", command=select_due_date, font=("Times New Roman", 13), bg="white")
            self.due_date_button.grid(row=1, column=7, padx=0, sticky="ew")

            self.due_time_button = Button(study, text="Select Due Time", command=select_time, font=("Times New Roman", 13), bg="white")
            self.due_time_button.grid(row=1, column=8, padx=0, sticky="ew")

            self.add_button = Button(study, text="Add", command=add_task, font=("Times New Roman", 13), bg="white")
            self.add_button.grid(row=1, column=9, padx=(0, 10), sticky="ew")
            self.selected_date = None
            self.selected_time = None
            self.study_frame = Frame(study, bg="white")
            self.study_frame.grid(row=2, column=0, columnspan=10, rowspan=9, padx=20, pady=10, sticky="nsew")

            self.study_label = Label(self.study_frame, text="To Do:", font=("Cooper Black", 30), bg="white")
            self.study_label.grid(row=0, column=0, columnspan=9, pady=5)

            self.task_widgets = []
            self.task_count = 0
            self.task_count_label = Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 10), bg="white")
            self.task_count_label.grid(row=1, column=0, padx=20, sticky="w")

            self.delete_all_button = Button(study, text="Delete All Task", command=delete_all_tasks, font=("Times New Roman", 10), bg="white")
            self.delete_all_button.grid(row=9, column=5, columnspan=4, pady=1)

            self.delete_selected_button = Button(study, text="Delete Selected Tasks", command=delete_selected_tasks)
            self.delete_selected_button.grid(row=9, column=3, columnspan=3, pady=1)
            self.calendar_tasks = {}

            # Initialize instance variables
            self.due_date_selected = False
            self.due_time_selected = False

              
#Change to Default Mode
        def switch_default_mode():
            root.config(bg="IndianRed")
            hide_frames()
            self.timer_lbl.grid(row=1,column=2, rowspan=6,columnspan=6,sticky="nsew")
            self.default_start_btn.grid(row=6, column =2,rowspan=3,columnspan=2,sticky="nsew")
            self.default_stop_btn.grid(row=6, column =4,rowspan=3,columnspan=2,sticky="nsew")
            self.default_reset_btn.grid(row=6, column =6,rowspan=3,columnspan=2,sticky="nsew")
            self.music_btn.grid(row=0, column=9, sticky="nsew")
            self.session_type_lbl.grid(row=3, column=9,sticky="nsew")
            self.session_type_img.grid(row=4, column=9,sticky="nsew")
            self.cycles_lbl.grid(row=9, column=1,sticky="nsew")
            self.current_tomato_lbl.grid(row=9, column=0,sticky="nsew")

#Change to Study Mode
        def study_mode():
            root.config(bg="Cornflowerblue")
            hide_frames()

            self.study_timer_lbl.grid(row=1,column=2, rowspan=6,columnspan=6,sticky="nsew")
            self.study_start_btn.grid(row=6, column =2,rowspan=3,columnspan=2,sticky="nsew")
            self.study_stop_btn.grid(row=6, column =4,rowspan=3,columnspan=2,sticky="nsew")
            self.study_reset_btn.grid(row=6, column =6,rowspan=3,columnspan=2,sticky="nsew")
            self.studysession_type_img.grid(row=4, column=9,sticky="nsew")
            self.study_session_type_lbl.grid(row=3, column=9,sticky="nsew")

#Change to Relax Mode
        def relax_mode():
            root.config(bg="mediumseagreen")
            hide_frames()

            self.relax_timer_lbl.grid(row=1,column=2, rowspan=6,columnspan=6,sticky="nsew")
            self.relax_start_btn.grid(row=6, column =2,rowspan=3,columnspan=2,sticky="nsew")
            self.relax_stop_btn.grid(row=6, column =4,rowspan=3,columnspan=2,sticky="nsew")
            self.relax_reset_btn.grid(row=6, column =6,rowspan=3,columnspan=2,sticky="nsew") 
            self.relaxsession_type_img.grid(row=4, column=9,sticky="nsew")
            self.relax_session_type_lbl.grid(row=3, column=9,sticky="nsew")

#Hide other mode buttons when switching mode
        def hide_frames():
            self.timer_lbl.grid_forget()
 
            self.default_start_btn.grid_forget()
            self.default_stop_btn.grid_forget()
            self.default_reset_btn.grid_forget()
            self.current_tomato_lbl.grid_forget()
            self.cycles_lbl.grid_forget()
            self.session_type_img.grid_forget()
            self.session_type_lbl.grid_forget()
            self.music_btn.grid_forget()

            self.study_timer_lbl.grid_forget()

            self.study_start_btn.grid_forget()
            self.study_stop_btn.grid_forget()
            self.study_reset_btn.grid_forget()
            self.study_session_type_lbl.grid_forget()
            self.studysession_type_img.grid_forget()

            self.relax_timer_lbl.grid_forget()

            self.relax_start_btn.grid_forget()
            self.relax_stop_btn.grid_forget()
            self.relax_reset_btn.grid_forget()
            self.relax_session_type_lbl.grid_forget()
            self.relaxsession_type_img.grid_forget()

        def open_color():
            # Open color picker dialog
            color = colorchooser.askcolor(title="Choose Color")
            new_bg_color = None  # Default value
            if color[1]:  # If a color is selected
                new_bg_color = color[1]  # Get the hexadecimal color code
            # Update background color of specified elements
            root.configure(bg=new_bg_color)
            self.default_start_btn.configure(bg=new_bg_color)
            self.default_stop_btn.configure(bg=new_bg_color)
            self.default_reset_btn.configure(bg=new_bg_color)
            self.timer_lbl.configure(bg=new_bg_color)
            self.music_btn.configure(bg=new_bg_color)
            self.cycles_lbl.configure(bg=new_bg_color)
            self.session_type_img.configure(bg=new_bg_color)
            self.session_type_lbl.configure(bg=new_bg_color)
            self.background_color = new_bg_color

        def update_volume(val):
            volume = int(val) / 100  # Scale to 0-1 for pygame
            pygame.mixer.music.set_volume(volume)
            self.volume_label.config(text=f": {val}%")

        def save_preset1_settings():
            save_preset_settings(1)

        def save_preset2_settings():
            save_preset_settings(2)

        def save_preset3_settings():
            save_preset_settings(3)

        def load_preset1_settings():
            load_preset_settings(1)

        def load_preset2_settings():
            load_preset_settings(2)

        def load_preset3_settings():
            load_preset_settings(3)

        def save_preset_settings(preset_number):
            # Retrieve settings from UI inputs
            try:
                timer_minutes = int(self.timer_entry.get())
                timer_seconds = int(self.timerseconds_entry.get())
                shortbreak_minutes = int(self.shortbreak_entry.get())
                shortbreak_seconds = int(self.shortbreakseconds_entry.get())
                longbreak_minutes = int(self.longbreak_entry.get())
                longbreak_seconds = int(self.longbreakseconds_entry.get())
                repeat_cycles = int(self.repeat_cycles_entry.get())
            except ValueError:
        # If any of the entries cannot be converted to an integer, show an error message
                messagebox.showerror("Input Error", "Please enter valid numbers in all entry boxes.")
                return

            timer_duration = timer_minutes * 60 + timer_seconds
            shortbreak_duration = shortbreak_minutes * 60 + shortbreak_seconds
            longbreak_duration = longbreak_minutes * 60 + longbreak_seconds

            selected_timer_end_sound = self.alarm_sound_combobox.get()
            selected_short_break_sound = self.SB_sound_combobox.get()
            selected_long_break_sound = self.LB_sound_combobox.get()

            self.timer_end_sound = self.sound_files[selected_timer_end_sound]
            self.short_break_sound = self.sound_files[selected_short_break_sound]
            self.long_break_sound = self.sound_files[selected_long_break_sound]

            self.default_timer_duration = timer_duration
            self.default_remaining_time = timer_duration

            self.default_shortbreak_duration = shortbreak_duration
            self.default_longbreak_duration = longbreak_duration

            self.initialize_cycles(repeat_cycles)

            self.number_cycles = repeat_cycles
            self.update_cycle_count_label()
            
            self.update_default_display()
            self.cycles_lbl.config(text="Cycles: {}".format(repeat_cycles))
            volume = self.volume_slider.get()

            # Check if the preset already exists
            self.cursor.execute("SELECT COUNT(*) FROM Presets WHERE ID = ?", (preset_number,))
            exists = self.cursor.fetchone()[0]

            if exists:
                # Update existing preset
                self.cursor.execute("""UPDATE Presets SET
                    TimerDuration = ?, ShortBreakDuration = ?, LongBreakDuration = ?, RepeatCycles = ?, TimerEndSound = ?, ShortBreakSound = ?, LongBreakSound = ?, BackgroundColor = ?, Volume = ?
                    WHERE ID = ?""",
                    (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                    self.timer_end_sound, self.short_break_sound, self.long_break_sound,
                    self.background_color, volume, preset_number))
                print(f"Preset '{preset_number}' settings updated successfully!")
            else:
                # Insert new preset
                self.cursor.execute("""INSERT INTO Presets (
                    ID, TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (preset_number, timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                self.timer_end_sound, self.short_break_sound, self.long_break_sound,
                self.background_color, volume))
                print(f"Preset '{preset_number}' settings saved successfully!")
            
            self.conn.commit()

        def load_preset_settings(preset_number):
            self.cursor.execute(
                "SELECT TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume FROM Presets WHERE ID = ?",
                (preset_number,)
            )
            row = self.cursor.fetchone()
            if row:
                # Unpack the row into variables
                (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                timer_end_sound, short_break_sound, long_break_sound, background_color, volume) = row

                # Update UI with loaded settings
                self.timer_entry.delete(0, END)
                self.timer_entry.insert(0, str(timer_duration // 60))  # minutes
                self.timerseconds_entry.delete(0, END)
                self.timerseconds_entry.insert(0, str(timer_duration % 60))  # seconds

                self.shortbreak_entry.delete(0, END)
                self.shortbreak_entry.insert(0, str(shortbreak_duration // 60))
                self.shortbreakseconds_entry.delete(0, END)
                self.shortbreakseconds_entry.insert(0, str(shortbreak_duration % 60))

                self.longbreak_entry.delete(0, END)
                self.longbreak_entry.insert(0, str(longbreak_duration // 60))
                self.longbreakseconds_entry.delete(0, END)
                self.longbreakseconds_entry.insert(0, str(longbreak_duration % 60))

                self.repeat_cycles_entry.delete(0, END)
                self.repeat_cycles_entry.insert(0, str(repeat_cycles))

                self.alarm_sound_combobox.set(timer_end_sound)
                self.SB_sound_combobox.set(short_break_sound)
                self.LB_sound_combobox.set(long_break_sound)

                self.default_timer_duration = timer_duration
                self.default_remaining_time = timer_duration

                self.default_shortbreak_duration = shortbreak_duration
                self.default_longbreak_duration = longbreak_duration

                self.initialize_cycles(repeat_cycles)

                self.timer_end_sound = timer_end_sound
                self.short_break_sound = short_break_sound
                self.long_break_sound = long_break_sound

                self.background_color = background_color
                self.volume = volume

                # Apply settings to UI
                self.root.configure(bg=background_color)
                self.timer_lbl.configure(bg=background_color)
                self.cycles_lbl.configure(bg=background_color)
                self.session_type_lbl.configure(bg=background_color)
                self.update_cycle_count_label()
                self.update_default_display()
                # Apply volume to volume slider
                self.volume_slider.set(volume)
                print(f"Preset {preset_number} settings loaded successfully!")
            else:
                print(f"No settings found for Preset {preset_number}.")

#Reset All Entry Boxes and Revert to Original Default Mode
        def reset_default_mode():
            self.default_remaining_time = 1500
            self.default_shortbreak_duration = 300
            self.default_longbreak_duration = 900
            self.update_default_display()

            self.default_remaining_time = self.default_timer_duration
            self.timer_type = "default_timer"

            self.number_cycles= 0
            self.current_cycle = 0
            self.update_cycle_count_label()
            self.cycles_lbl.config(text="Cycles: 0")

            self.timer_entry.delete(0,END)
            self.timer_entry.insert(0,"25")
            self.timerseconds_entry.delete(0, END)
            self.timerseconds_entry.insert(0,"00")
            self.shortbreak_entry.delete(0,END)
            self.shortbreak_entry.insert(0,"5")
            self.shortbreakseconds_entry.delete(0,END)
            self.shortbreakseconds_entry.insert(0,"00")
            self.longbreak_entry.delete(0,END)
            self.longbreak_entry.insert(0,"15")
            self.longbreakseconds_entry.delete(0,END)
            self.longbreakseconds_entry.insert(0,"00")
            self.repeat_cycles_entry.delete(0,END)

            root.configure(bg="IndianRed")
            self.timer_lbl.configure(bg="IndianRed")
            self.cycles_lbl.configure(bg="IndianRed")
            self.session_type_lbl.configure(bg="IndianRed")

            self.alarm_sound_combobox.set("Default Alarm")
            self.SB_sound_combobox.set("Default Short Break")
            self.LB_sound_combobox.set("Default Microwave")

            self.timer_end_sound = self.sound_files["Default Alarm"]
            self.short_break_sound = self.sound_files["Default Short Break"]
            self.long_break_sound = self.sound_files["Default Microwave"]
            self.volume = 50
            # Reset volume slider to 50
            self.volume_slider.set(50)
            # Reset all three presets to original defaults
            for preset_number in range(1, 4):
                # Get the original default settings for each preset from the Presets table
                self.cursor.execute(
                    "SELECT TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume FROM Presets WHERE ID = ?",
                    (preset_number,)
                )
                row = self.cursor.fetchone()
                if row:
                    # Unpack the row into variables
                    (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                    timer_end_sound, short_break_sound, long_break_sound, background_color, volume) = row

                    # Update the preset with the original default values
                    self.cursor.execute("""UPDATE Presets SET
                        TimerDuration = ?, ShortBreakDuration = ?, LongBreakDuration = ?, RepeatCycles = ?, TimerEndSound = ?, ShortBreakSound = ?, LongBreakSound = ?, BackgroundColor = ?, Volume = ?
                        WHERE ID = ?""",
                        (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                        timer_end_sound, short_break_sound, long_break_sound,
                        "IndianRed", 50, preset_number))  # Hardcode default background color and volume

                    # Commit changes to the database
                    self.conn.commit()

            # Commit changes to the database after resetting all presets
            self.conn.commit()

#Settings Window
        def open_settings():
            global counter

    #Limiting Settings Window to only be opened one time
            if counter <2:
                settings_window = Toplevel(root)
                settings_window.title("Settings")
                settings_window.geometry("500x500")
                settings_window.configure(bg ="gray")

                self.settingswindow_icon = PhotoImage(file="user setting1.png")
                settings_window.iconphoto(False,self.settingswindow_icon)       

                settings_window.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
                settings_window.rowconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform='a')

    #TIMER DURATION ENTRYBOX
                self.timersetting_icon = PhotoImage(file="timer.png")
                self.timersetting_img_lbl = Label(settings_window, image=self.timersetting_icon,bg="gray")
                self.timersetting_img_lbl.grid(row = 0, column=0,sticky="w")
                self.timer_entry_lbl= Label(settings_window, text="Timer Duration:", font=("Arial",18), bg="gray", fg="black")
                self.timer_entry_lbl.grid(row = 0, column=1,columnspan=2, sticky="w")

                self.timer_entry = Entry(settings_window, font=("Arial",13), bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.timer_entry.grid(row = 0, column=3, columnspan=1,sticky="w")
                self.timer_entry.insert(0,"25")

                self.timerseconds_entry = Entry(settings_window, font=("Arial",13),bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.timerseconds_entry.grid(row = 0, column=4, columnspan =1,sticky="w")
                self.timerseconds_entry.insert(0,"00")

    #SHORT BREAK DURATION ENTRYBOX
                self.shortbreaksetting_icon = PhotoImage(file="short break.png")
                self.shortbreaksetting_img_lbl = Label(settings_window, image=self.shortbreaksetting_icon,bg="gray")
                self.shortbreaksetting_img_lbl.grid(row = 1, column=0,sticky="w")
                self.shortbreak_entry_lbl= Label(settings_window, text="Short Break Duration:", font=("Arial",18), bg="gray", fg="black")
                self.shortbreak_entry_lbl.grid(row = 1, column=1, columnspan=2, sticky="w")

                self.shortbreak_entry = Entry(settings_window, font=("Arial",13), bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.shortbreak_entry.grid(row = 1, column=3, columnspan=1,sticky="w")
                self.shortbreak_entry.insert(0,"5")

                self.shortbreakseconds_entry = Entry(settings_window, font=("Arial",13),bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.shortbreakseconds_entry.grid(row = 1, column=4, columnspan=1,sticky="w")
                self.shortbreakseconds_entry.insert(0, "00")

    #LONG BREAK DURATION ENTRYBOX
                self.longbreaksetting_icon = PhotoImage(file="long break.png")
                self.longbreaksetting_img_lbl = Label(settings_window, image=self.longbreaksetting_icon,bg="gray")
                self.longbreaksetting_img_lbl.grid(row =2, column=0,sticky="w")
                self.longbreak_entry_lbl= Label(settings_window, text="Long Break Duration:", font=("Arial",18), bg="gray", fg="black")
                self.longbreak_entry_lbl.grid(row = 2, column=1, columnspan=2, sticky="w")

                self.longbreak_entry = Entry(settings_window, font=("Arial",13),bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.longbreak_entry.grid(row = 2, column=3, columnspan=1,sticky="w")
                self.longbreak_entry.insert(0,"15")

                self.longbreakseconds_entry = Entry(settings_window, font=("Arial",13),bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.longbreakseconds_entry.grid(row = 2, column=4, columnspan=1,sticky="w")
                self.longbreakseconds_entry.insert(0, "00")

    #REPEAT CYCLES ENTRYBOX
                self.repeat_cycles_icon = PhotoImage(file="tomato cycle.png")
                self.repeat_cycles_img_lbl = Label(settings_window, image=self.repeat_cycles_icon,bg="gray")
                self.repeat_cycles_img_lbl.grid(row =3, column=0,sticky="w")
                self.repeat_cycles_lbl= Label(settings_window, text="Times to Repeat:", font=("Arial",18), bg="gray", fg="black")
                self.repeat_cycles_lbl.grid(row = 3, column=1, columnspan=2, sticky="w")

                self.repeat_cycles_entry = Entry(settings_window, font=("Arial",13),bg="lightgray",width=7,borderwidth=4, relief="sunken",highlightthickness=2, highlightbackground="gray",highlightcolor="black")
                self.repeat_cycles_entry.grid(row = 3, column=3, columnspan=1,sticky="w")

    #RESET PRESETS
                self.reset_all_icon = PhotoImage(file="reset all.png")
                self.reset_all_btn=Button(settings_window,text="Reset ALL Presets",font=("Arial",13),compound="top", image=self.reset_all_icon, command=reset_default_mode,borderwidth=0,bg="gray", activebackground ="gray", highlightthickness=0)
                self.reset_all_btn.grid(row=8,column=8,columnspan=2,rowspan=2,sticky="se")

    #ENDING SOUNDS COMBOBOX
                self.sounds_icon = PhotoImage(file="sounds setting.png")
                self.sounds_img_lbl = Label(settings_window, image=self.sounds_icon,bg="gray")
                self.sounds_img_lbl.grid(row =4, column=0,sticky="w")
                self.sounds_entry_lbl= Label(settings_window, text="Ending Sounds:", font=("Arial",18), bg="gray", fg="black")
                self.sounds_entry_lbl.grid(row = 4, column=1,columnspan=2, sticky="w")

                alarm_options = ["Default Alarm","Referee Whistle","Chime","Default Short Break","Churchbell","Wind Chimes","Default Microwave", "Great Harp", "Relaxing Harp"]
                SB_options = ["Default Short Break", "Churchbell", "Wind Chimes","Default Alarm","Referee Whistle","Chime","Default Microwave", "Great Harp", "Relaxing Harp"]
                LB_options = ["Default Microwave", "Great Harp", "Relaxing Harp","Default Alarm","Referee Whistle","Chime","Default Short Break","Churchbell","Wind Chimes"]

                self.alarm_sound_combobox = ttk.Combobox(settings_window, values=alarm_options, font=("Arial",13),width=13)
                self.alarm_sound_combobox.current(0)
                self.alarm_sound_combobox.grid(row=4, column=3, columnspan=2,sticky="w")

                self.SB_sound_combobox = ttk.Combobox(settings_window, values=SB_options, font=("Arial",13),width=13)
                self.SB_sound_combobox.current(0)
                self.SB_sound_combobox.grid(row=4, column=5, columnspan=2,sticky="w")

                self.LB_sound_combobox = ttk.Combobox(settings_window, values=LB_options, font=("Arial",13),width=13)
                self.LB_sound_combobox.current(0)
                self.LB_sound_combobox.grid(row=4, column=7, columnspan=2,sticky="w")

                self.alarm_sound_combobox.bind("<<ComboboxSelected>>")
                self.SB_sound_combobox.bind("<<ComboboxSelected>>")
                self.LB_sound_combobox.bind("<<ComboboxSelected>>")

                self.selected_alarm_sound = "Default Alarm"
                self.selected_SB_sound = "Default Short Break"
                self.selected_LB_sound = "Default Microwave LB"

    #BACKGROUND COLOR
                self.backgroundcolor_icon = PhotoImage(file="bg color.png")
                self.backgroundcolor_img_lbl = Label(settings_window, image=self.backgroundcolor_icon,bg="gray")
                self.backgroundcolor_img_lbl.grid(row =5, column=0,sticky="w")
                self.bg_color_lbl = Label(settings_window, text="Background Color:", font=("Arial",18), bg="gray", fg="black")
                self.bg_color_lbl.grid(row = 5, column=1,columnspan=2, sticky="w")

                self.bg_color_btn = Button(settings_window, text="Background Color", font=("Arial",13), bg="indianred", fg="black",activebackground="white", command=open_color)
                self.bg_color_btn.grid(row=5, column=3, columnspan=2, sticky="w")

    #VOLUME SLIDER
                self.volume_icon = PhotoImage(file="volume.png")
                self.volume_img_lbl = Label(settings_window, image=self.volume_icon,bg="gray")
                self.volume_img_lbl.grid(row =6, column=0,sticky="w")
                volume_label = Label(settings_window, text="Sound Volume:", font=("Arial", 18), bg="gray", fg="black")
                volume_label.grid(row=6, column=1, columnspan=3, sticky="w")

                self.volume_slider = Scale(settings_window, from_=0, to=100, orient=HORIZONTAL, command=update_volume, font=("Arial", 13))
                self.volume_slider.set(self.volume)
                self.volume_slider.grid(row=6, column=2, columnspan=3)

                self.volume2_icon = PhotoImage(file="vol lbl.png")
                self.volume_label = Label(settings_window,text="",image=self.volume2_icon,compound="left", font=("Courier New", 16,"bold"), fg="black", bg="gray")
                self.volume_label.grid(row=6, column=5, columnspan=2, sticky="w")

    #PRESET 1 (SAVE AND LOAD)
                self.preset1_icon = PhotoImage(file="preset 1.png")
                self.preset1_img_lbl = Label(settings_window, image=self.preset1_icon,bg="gray")
                self.preset1_img_lbl.grid(row=7,column=0,sticky="w")

                self.preset1_label = Label(settings_window, text="Preset 1:", font=("Arial", 18), bg="gray", fg="black")
                self.preset1_label.grid(row=7, column=1, columnspan=2, sticky="w")

                self.save_preset1_icon = PhotoImage(file="save preset1.png")

                self.save_preset1_btn=Button(settings_window, image=self.save_preset1_icon,bg="gray",command=save_preset1_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.save_preset1_btn.grid(row=7,column=3,columnspan=1,sticky="w")

                self.load_preset1_icon = PhotoImage(file="load preset1.png")

                self.load_preset1_btn=Button(settings_window, image=self.load_preset1_icon,bg="gray",command=load_preset1_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.load_preset1_btn.grid(row=7,column=4,columnspan=1,sticky="w")

    #PRESET 2 (SAVE AND LOAD)
                self.preset2_icon = PhotoImage(file="preset 2.png")
                self.preset2_img_lbl = Label(settings_window, image=self.preset2_icon,bg="gray")
                self.preset2_img_lbl.grid(row=8,column=0,sticky="w")

                self.preset2_label = Label(settings_window, text="Preset 2:", font=("Arial", 18), bg="gray", fg="black")
                self.preset2_label.grid(row=8, column=1, columnspan=2, sticky="w")

                self.save_preset2_icon = PhotoImage(file="save preset2.png")

                self.save_preset2_btn=Button(settings_window, image=self.save_preset2_icon,bg="gray",command=save_preset2_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.save_preset2_btn.grid(row=8,column=3,columnspan=1,sticky="w")

                self.load_preset2_icon = PhotoImage(file="load preset2.png")

                self.load_preset2_btn=Button(settings_window, image=self.load_preset2_icon,bg="gray",command=load_preset2_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.load_preset2_btn.grid(row=8,column=4,columnspan=1,sticky="w")

    #PRESET 3 (SAVE AND LOAD)
                self.preset3_icon = PhotoImage(file="preset 3.png")
                self.preset3_img_lbl = Label(settings_window, image=self.preset3_icon,bg="gray")
                self.preset3_img_lbl.grid(row=9,column=0,sticky="w")

                self.preset3_label = Label(settings_window, text="Preset 3:", font=("Arial", 18), bg="gray", fg="black")
                self.preset3_label.grid(row=9, column=1, columnspan=2, sticky="w")

                self.save_preset3_icon = PhotoImage(file="save preset3.png")

                self.save_preset3_btn=Button(settings_window, image=self.save_preset3_icon,bg="gray",command=save_preset3_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.save_preset3_btn.grid(row=9,column=3,columnspan=1,sticky="w")

                self.load_preset3_icon = PhotoImage(file="load preset3.png")

                self.load_preset3_btn=Button(settings_window, image=self.load_preset3_icon,bg="gray",command=load_preset3_settings,borderwidth=0,activebackground ="gray", highlightthickness=0)
                self.load_preset3_btn.grid(row=9,column=4,columnspan=1,sticky="w")

                counter+=1
            else: 
                messagebox.showinfo("Error","There is already a Settings window opened.")


#MENU Taskbar Main Interface
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

     #User Menu (Statistics, Achievements,Study List)
        user_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="User", menu=user_menu)
        self.statistics_icon=PhotoImage(file="statistics.png")
        user_menu.add_command(label="Statistics",image=self.statistics_icon,compound="left", command=user_data)
        self.achievements_icon=PhotoImage(file="achievements.png")
        user_menu.add_separator()
        self.studylist_icon=PhotoImage(file="studylist.png")
        user_menu.add_command(label="Study List",image=self.studylist_icon,compound="left", command=studylist_user)

    #Mode Menu (Default, Study, Relax)
        mode_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        self.default_icon=PhotoImage(file="defaultmode.png")
        mode_menu.add_command(label="Default Mode",image=self.default_icon,compound="left", command=switch_default_mode)
        mode_menu.add_separator()
        self.study_icon=PhotoImage(file="studymode.png")
        mode_menu.add_command(label="Study Mode",image=self.study_icon,compound="left", command=study_mode)
        mode_menu.add_separator()
        self.relax_icon=PhotoImage(file="relaxmode.png")
        mode_menu.add_command(label="Relax Mode",image=self.relax_icon,compound="left", command=relax_mode)

    #Settings Open(Open new settings window)
        setting_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Settings",menu=setting_menu)
        self.opensettings_icon=PhotoImage(file="open settings.png")
        setting_menu.add_command(label="Open",image=self.opensettings_icon,compound="left", command=open_settings)

    #Default Mode Buttons and Label
        self.timer_lbl = Label(root, text = "25:00", font= ("Digital-7", 150,), fg ="black", bg = "IndianRed")

        self.current_tomato_lbl = Label(root,text="Current\nCycles",font=("Courier New", 20,"bold"), fg="black", bg="IndianRed")
        self.tomato_cycle_icon = PhotoImage(file="tomato cycle.png")
        self.cycles_lbl = Label(root, text="",image=self.tomato_cycle_icon,compound="left", font=("Courier New", 20,"bold"), fg="black", bg="IndianRed")

        self.start_icon = PhotoImage(file="start2.png")
        self.stop_icon = PhotoImage(file="stop.png")
        self.reset_icon = PhotoImage(file="repeat3.png")

        self.default_start_btn = Button(root, image=self.start_icon,command =self.start_default_time, borderwidth=0,bg="indianred", activebackground ="indianred", highlightthickness=0, relief='flat')
        self.default_stop_btn = Button(root,image=self.stop_icon,command =self.pause_default_time,borderwidth=0,bg="indianred",activebackground ="indianred", highlightthickness=0, relief='flat')
        self.default_reset_btn = Button(root,image=self.reset_icon,command =self.reset_default_time,borderwidth=0,bg="indianred",activebackground ="indianred", highlightthickness=0, relief='flat')

    #Study Mode Buttons and Label
        self.study_timer_lbl = Label(root, text ="45:00", font=("Digital-7", 150,), fg ="black", bg = "cornflowerblue")

        self.study_start_btn = Button(root, image=self.start_icon,command =self.start_study_time,borderwidth=0,bg="cornflowerblue", activebackground ="cornflowerblue", highlightthickness=0, relief='flat')
        self.study_stop_btn = Button(root,image=self.stop_icon,command =self.pause_study_time,borderwidth=0,bg="cornflowerblue", activebackground ="cornflowerblue", highlightthickness=0, relief='flat')
        self.study_reset_btn = Button(root,image=self.reset_icon,command =self.reset_study_time,borderwidth=0,bg="cornflowerblue", activebackground ="cornflowerblue", highlightthickness=0, relief='flat')
    
    #Relax Mode Label and Buttons
        self.relax_timer_lbl = Label(root, text ="15:00", font=("Digital-7", 150,), fg ="black", bg = "mediumseagreen")

        self.relax_start_btn = Button(root, image=self.start_icon,command =self.start_relax_time,borderwidth=0,bg="mediumseagreen", activebackground ="mediumseagreen", highlightthickness=0, relief='flat')
        self.relax_stop_btn = Button(root,image=self.stop_icon,command =self.pause_relax_time,borderwidth=0,bg="mediumseagreen", activebackground ="mediumseagreen", highlightthickness=0, relief='flat')
        self.relax_reset_btn = Button(root,image=self.reset_icon,command =self.reset_relax_time,borderwidth=0,bg="mediumseagreen", activebackground ="mediumseagreen", highlightthickness=0, relief='flat')

        self.timer_icon = PhotoImage(file="timer.png")
        self.shortbreak_icon = PhotoImage(file="short break.png")
        self.longbreak_icon = PhotoImage(file="long break.png")

        self.session_type_img = Label(root, image=self.timer_icon,borderwidth=0,bg="indianred")
        self.session_type_lbl = Label(root, text="", font=("Courier New", 20,"bold"), fg="black", bg="IndianRed")

        self.studysession_type_img = Label(root, image=self.timer_icon,borderwidth=0,bg="cornflowerblue")
        self.study_session_type_lbl = Label(root, text="", font=("Courier New", 20,"bold"), fg="black", bg="cornflowerblue")

        self.relaxsession_type_img = Label(root, image=self.timer_icon,borderwidth=0,bg="mediumseagreen")
        self.relax_session_type_lbl = Label(root, text="", font=("Courier New", 20,"bold"), fg="black", bg="mediumseagreen") 

        self.tomato_cycle_icon = PhotoImage(file="tomato cycle.png")
        self.cycles_lbl = Label(root, text="",image=self.tomato_cycle_icon,compound="left", font=("Times", 16), fg="black", bg="IndianRed")
    
# Add background music button
        self.music_on_icon = PhotoImage(file="music on.png")
        self.music_off_icon = PhotoImage(file="music off.png")
        self.music_btn = Button(root,image=self.music_on_icon,command=self.toggle_music,borderwidth=0,bg="indianred", activebackground ="indianred", highlightthickness=0, relief='flat')

#Main Interface to show Default Mode first
        switch_default_mode()

###########################################################################################################
#DEFAULT#

# Default mode timer variables
        self.default_run_timer = False
        self.default_start_timer = 0
        self.default_pause_timer = False
        self.default_timer_duration = 1500
        self.default_remaining_time = self.default_timer_duration
        self.default_shortbreak_duration = 300  # Default short break duration in seconds
        self.default_longbreak_duration = 900   # Default long break duration in seconds

        self.timer_type = "default_timer"

        self.default_timer_sound = "Default Timer Alarm.wav"
        self.default_short_break_sound = "Default SB.wav"
        self.default_long_break_sound = "Default Microwave LB.wav"

        self.number_cycles = 0  # Initialize number of cycles to zero
        self.current_cycle = 0  #Current cycles is zero
        self.update_cycle_count_label()

#Music Button Toggle ON/OFF
    def toggle_music(self):
        if self.is_music_playing:
            pygame.mixer.music.stop()
            self.is_music_playing = False
            self.music_btn.config(image=self.music_on_icon)
        else:
            pygame.mixer.music.load("Autumn Garden.mp3")  # Replace with your background music file
            pygame.mixer.music.play(-1)  # Play the music indefinitely
            self.is_music_playing = True
            self.music_btn.config(image=self.music_off_icon)

    def defaultmode_timer(self): #25 mins
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "default_timer"
        self.start_default_time()

    def defaultmode_shortbreak(self): #5 mins
        self.default_timer_duration = self.default_shortbreak_duration
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "short_break"
        self.start_default_time()

    def defaultmode_longbreak(self): #15 mins
        self.default_timer_duration = self.default_longbreak_duration
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "long_break"
        self.start_default_time()

    # Default mode timer functions
    def start_default_time(self):
        if not self.default_run_timer:
            self.default_run_timer = True
            self.default_start_timer = time.time()
            self.update_default_time()

    def pause_default_time(self):
        if self.default_run_timer:
            self.default_run_timer = False

    def reset_default_time(self):
        self.default_run_timer = False
        if self.timer_type == "default_timer":
            self.default_remaining_time = self.default_timer_duration
        elif self.timer_type == "short_break":
            self.default_remaining_time = self.default_shortbreak_duration
        else:
            self.default_remaining_time = self.default_longbreak_duration
        self.update_default_display()

    def start_cycle(self):
        if self.number_cycles > 0:
            cycle_sequence_length = 9  # Length of the cycle sequence
            current_cycle_in_sequence = self.current_cycle % cycle_sequence_length
            
            # Determine the phase of the current cycle based on the sequence
            if current_cycle_in_sequence % 9 != 8:  # Timer or Short Break phase
                if current_cycle_in_sequence % 2 == 0:  # Timer phase
                    self.timer_type = "default_timer"
                    self.default_remaining_time = self.default_timer_duration
                    self.start_default_time()  # Start the timer
                else:  # Short break phase
                    self.timer_type = "short_break"
                    self.default_remaining_time = self.default_shortbreak_duration
                    self.start_default_time()  # Start the short break
            else:  # Long break phase
                self.timer_type = "long_break"
                self.default_remaining_time = self.default_longbreak_duration
                self.start_default_time()  # Start the long break
                # Reset current cycle to 0 after Long Break
                self.current_cycle = 0
                # Update cycle count label
                self.number_cycles -= 1
                self.update_cycle_count_label()
                return  # Skip the rest of the method after the long break

        else:
            # Handle case when no cycles left
            self.number_cycles = 0
            self.update_cycle_count_label()  # Update cycle count label

        self.current_cycle += 1

    def update_default_time(self):
        if self.default_run_timer:
            current_time = time.time()  # Get current time and find the time passed since it started
            time_passed = current_time - self.default_start_timer
            self.default_remaining_time = max(self.default_remaining_time - time_passed, 0)  # Prevents remaining time from becoming less than 0
            self.update_default_display()

            if self.default_remaining_time > 0:
                self.default_start_timer = current_time
                self.root.after(1000, self.update_default_time)
            else:
                # Timer has ended
                self.default_run_timer = False
                self.alarm_sound(self.timer_type)

                # Calculate cumulative time and check for achievements
                self.cumulative_time += self.default_timer_duration  # Adjust based on session type
                self.check_achievements()

                if self.timer_type == "default_timer":
                    self.complete_pomodoro_session("Default", self.default_timer_duration, None, "Timer")
                elif self.timer_type == "short_break":
                    self.complete_pomodoro_session("Default", self.default_shortbreak_duration, None, "Short Break")
                elif self.timer_type == "long_break":
                    self.complete_pomodoro_session("Default", self.default_longbreak_duration, None, "Long Break")

                # Wait for the sound to finish before starting the next session
                sound_length = pygame.mixer.Sound(self.timer_end_sound).get_length() * 1000  # Convert seconds to milliseconds
                self.root.after(int(sound_length), self.start_cycle) 
                self.update_default_display()
                # Update cycle count label
                self.update_cycle_count_label()

    # Call this method to start the pomodoro cycles
    def initialize_cycles(self, number_of_cycles):
        self.number_cycles = number_of_cycles  # Initialize number of cycles
        self.current_cycle = 0
        self.start_cycle()

    def update_default_display(self):
        minutes = int(self.default_remaining_time // 60)
        seconds = int(self.default_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)
        self.update_session_type_label()

    def update_cycle_count_label(self):
        # Ensure cycle count doesn't go below zero
        self.number_cycles = max(self.number_cycles, 0)
        self.cycles_lbl.config(text=": {}".format(self.number_cycles),font=("Times", 20))

    def update_session_type_label(self):
        # Update session type label based on the current session type
        if self.timer_type == "default_timer":
            self.session_type_img.config(image=self.timer_icon)
            self.session_type_lbl.config(text="Timer")
        elif self.timer_type == "short_break":
            self.session_type_img.config(image=self.shortbreak_icon)
            self.session_type_lbl.config(text="Short\nBreak")
        elif self.timer_type == "long_break":
            self.session_type_img.config(image=self.longbreak_icon)
            self.session_type_lbl.config(text="Long\nBreak")
   
    def alarm_sound(self, timer_type):
        if timer_type == "default_timer":
            self.play_sound(self.timer_end_sound)
        elif timer_type == "short_break":
            self.play_sound(self.short_break_sound)
        elif timer_type == "long_break":
            self.play_sound(self.long_break_sound)

    def play_sound(self, sound_file):
        # Pause the background music if it is playing
        if self.is_music_playing:
            pygame.mixer.music.pause()
        
        # Load and play the ending sound
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        
        # Resume the background music after the sound finishes
        sound_length = sound.get_length() * 1000  # Convert seconds to milliseconds
        self.root.after(int(sound_length), self.resume_music)

    def resume_music(self):
        if self.is_music_playing:
            pygame.mixer.music.unpause()

    def check_achievements(self):
        for threshold, badge_path in self.badges.items():
            if self.cumulative_time >= threshold and badge_path not in self.collected_badges:
                self.collected_badges.append(badge_path)
                self.achievement_unlocked(badge_path)

    def achievement_unlocked(self, badge_path):
        messagebox.showinfo("Achievement Unlocked!", "You've earned a new badge!")
        self.display_badge(badge_path)

    def display_badge(self, badge_path):
        badge_window = Toplevel(root)
        badge_window.title(f"{badge_path}")
        
        badge_image_tk = PhotoImage(file=badge_path)
        
        badge_label = Label(badge_window, image=badge_image_tk)
        badge_label.image = badge_image_tk
        badge_label.pack()

#################################################################################################################
#STUDY#

# Study mode timer variables
        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_shortbreak_duration = 900
        self.study_longbreak_duration = 1500

        self.study_type = "study_timer"
        self.study_cycle_count = 0

        #Load sounds
        self.study_timer_sound = pygame.mixer.Sound("Study Referee Alarm.wav")
        self.study_shortbreak_sound = pygame.mixer.Sound("Study Churchbell SB.wav")
        self.study_longbreak_sound = pygame.mixer.Sound("Study Great Harp LB.wav")


##STUDY MODE
    def studymode_timer(self): #45 mins
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_timer"

    def studymode_shortbreak(self): #15 mins
        self.study_timer_duration = self.study_shortbreak_duration
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_shortbreak"

    def studymode_longbreak(self): #25 mins
        self.study_timer_duration = self.study_longbreak_duration
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_longbreak"

##Study Mode BUTTON FUNCTIONALITY
    def start_study_time(self):
        if not self.study_run_timer:
            self.study_run_timer = True
            self.study_start_timer = time.time()
            self.update_study_time()

    def pause_study_time(self):
        if self.study_run_timer:
            self.study_run_timer = False

    def reset_study_time(self):
        self.study_run_timer = False
        if self.study_type == "study_timer":
            self.study_remaining_time = self.study_timer_duration
        elif self.study_type == "study_shortbreak":
            self.study_remaining_time = self.study_shortbreak_duration
        else:
            self.study_remaining_time = self.study_longbreak_duration
        self.study_remaining_time = self.study_timer_duration
        self.update_study_display()

    def update_study_time(self):
        if self.study_run_timer:
            current_time = time.time()
            time_passed = current_time - self.study_start_timer
            self.study_remaining_time = max(self.study_remaining_time - time_passed, 0)
            self.update_study_display()

            if self.study_remaining_time > 0:
                self.study_start_timer = current_time
                self.root.after(1000, self.update_study_time)
            else:
                self.study_run_timer = False
                self.alarm_sound2(self.study_type)


                if self.study_type == "study_timer":
                    self.study_type = "study_shortbreak"
                    self.study_remaining_time = self.study_shortbreak_duration
                    self.complete_pomodoro_session("Study", self.study_shortbreak_duration, None, "Short Break")
                    self.start_study_time()  # Start short break timer automatically
                elif self.study_type == "study_shortbreak":
                    self.study_cycle_count += 1
                    if self.study_cycle_count < 4:
                        self.study_type = "study_timer"
                        self.study_remaining_time = self.study_timer_duration
                        self.complete_pomodoro_session("Study", self.study_timer_duration, None, "Timer")
                        self.start_study_time()  # Start timer automatically
                    else:
                        self.study_type = "study_longbreak"
                        self.study_remaining_time = self.study_longbreak_duration
                        self.complete_pomodoro_session("Study", self.study_longbreak_duration, None, "Long Break")
                        self.study_cycle_count = 0  # Reset cycle count after long break
                        self.start_study_time()  # Start long break timer automatically
                        # Calculate the length of the sound file in milliseconds
                # Update the display with the new timer type and remaining time
                self.update_study_display()


    def update_study_display(self):
        minutes = int(self.study_remaining_time // 60)
        seconds = int(self.study_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.study_timer_lbl.config(text=time_str)
        self.update_study_session_type_label()

    def update_study_session_type_label(self):
        # Update session type label based on the current session type
        if self.study_type == "study_timer":
            self.studysession_type_img.config(image=self.timer_icon)
            self.study_session_type_lbl.config(text="Timer")
        elif self.study_type == "study_shortbreak":
            self.studysession_type_img.config(image=self.shortbreak_icon)
            self.study_session_type_lbl.config(text="Short\nBreak")
        elif self.study_type == "study_longbreak":
            self.studysession_type_img.config(image=self.longbreak_icon)
            self.study_session_type_lbl.config(text="Long\nBreak")

    def alarm_sound2(self,study_type):
        # Stop any currently playing sound
        pygame.mixer.stop()

        if study_type == "study_timer":
            self.study_timer_sound.play()
        elif study_type == "study_shortbreak":
            self.study_shortbreak_sound.play()
        elif study_type == "study_longbreak":
            self.study_longbreak_sound.play()

#########################################################################################################33
#RELAX#
        # Relax mode timer variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_shortbreak_duration = 1200
        self.relax_longbreak_duration = 1800

        self.relax_type = "relax_timer"
        self.relax_cycle_count = 0

        #Load sounds
        self.relax_timer_sound = pygame.mixer.Sound("Relax Chime Alarm.wav")
        self.relax_shortbreak_sound = pygame.mixer.Sound("Relax WindChimes SB.wav")
        self.relax_longbreak_sound = pygame.mixer.Sound("Relax Harp LB.wav")

##RELAX
    def relaxmode_timer(self): #15 mins
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_timer"          

    def relaxmode_shortbreak(self): #20 mins
        self.relax_timer_duration = self.relax_shortbreak_duration
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_shortbreak"  

    def relaxmode_longbreak(self): #30 mins
        self.relax_timer_duration = self.relax_longbreak_duration
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_longbreak"  

##Relax mode timer functions
    def start_relax_time(self):
        if not self.relax_run_timer:
            self.relax_run_timer = True
            self.relax_start_timer = time.time()
            self.update_relax_time()

    def pause_relax_time(self):
        if self.relax_run_timer:
            self.relax_run_timer = False

    def reset_relax_time(self):
        self.relax_run_timer = False
        if self.relax_type == "study_timer":
            self.relax_remaining_time = self.relax_timer_duration
        elif self.relax_type == "study_shortbreak":
            self.relax_remaining_time = self.relax_shortbreak_duration
        else:
            self.relax_remaining_time = self.relax_longbreak_duration
        self.relax_remaining_time = self.relax_timer_duration
        self.update_relax_display()

    def update_relax_time(self):
        if self.relax_run_timer:
            current_time = time.time()
            time_passed = current_time - self.relax_start_timer
            self.relax_remaining_time = max(self.relax_remaining_time - time_passed, 0)
            self.update_relax_display()

            if self.relax_remaining_time > 0:
                self.relax_start_timer = current_time
                self.root.after(1000, self.update_relax_time)
            else:
                self.relax_run_timer = False
                self.alarm_sound3(self.relax_type)

                if self.relax_type == "relax_timer":
                    self.relax_type = "relax_shortbreak"
                    self.relax_remaining_time = self.relax_shortbreak_duration
                    self.complete_pomodoro_session("Relax", self.relax_shortbreak_duration, None, "Short Break")
                    self.start_relax_time()  # Start short break timer automatically
                elif self.relax_type == "relax_shortbreak":
                    self.relax_cycle_count += 1
                    if self.relax_cycle_count < 4:
                        self.relax_type = "relax_timer"
                        self.relax_remaining_time = self.relax_timer_duration
                        self.complete_pomodoro_session("Relax", self.study_timer_duration, None, "Timer")
                        self.start_relax_time()  # Start timer automatically
                    else:
                        self.relax_type = "relax_longbreak"
                        self.relax_remaining_time = self.relax_longbreak_duration
                        self.complete_pomodoro_session("Relax", self.study_longbreak_duration, None, "Long Break")
                        self.relax_cycle_count = 0  # Reset cycle count after long break
                        self.start_relax_time()  # Start long break timer automatically

                # Update the display with the new timer type and remaining time
                self.update_relax_display()


    def update_relax_display(self):
        minutes = int(self.relax_remaining_time // 60)
        seconds = int(self.relax_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.relax_timer_lbl.config(text=time_str)
        self.update_relax_session_type_label()

    def update_relax_session_type_label(self):
        # Update session type label based on the current session type
        if self.relax_type == "relax_timer":
            self.relaxsession_type_img.config(image=self.timer_icon)
            self.relax_session_type_lbl.config(text="Timer")
        elif self.relax_type == "relax_shortbreak":
            self.relaxsession_type_img.config(image=self.shortbreak_icon)
            self.relax_session_type_lbl.config(text="Short\nBreak")
        elif self.relax_type == "relax_longbreak":
            self.relaxsession_type_img.config(image=self.longbreak_icon)
            self.relax_session_type_lbl.config(text="Long\nBreak")

    def alarm_sound3(self,relax_type):
        # Stop any currently playing sound
        pygame.mixer.stop()

        if relax_type == "relax_timer":
            self.relax_timer_sound.play()
        elif relax_type == "relax_shortbreak":
            self.relax_shortbreak_sound.play()
        elif relax_type == "relax_longbreak":
            self.relax_longbreak_sound.play()

    def insert_pomodoro_session(self, mode, session_type, duration, user='John'):
        completion_time = datetime.now().isoformat()  # Get the current completion time

        # Execute the SQL query to insert the session into the table
        self.cursor.execute('''
            INSERT INTO PomodoroSessions (User, Mode, SessionType, Duration, CompletionTime)
            VALUES (?, ?, ?, ?, ?)
        ''', (user, mode, session_type, duration, completion_time))
        self.conn.commit()

    def complete_pomodoro_session(self, mode, timer_duration, short_break_duration=None, long_break_duration=None):
        self.insert_pomodoro_session(mode, 'Timer', timer_duration)
        if short_break_duration is not None:
            self.insert_pomodoro_session(mode, 'Short Break', short_break_duration)
        if long_break_duration is not None:
            self.insert_pomodoro_session(mode, 'Long Break', long_break_duration)
        self.conn.commit()

    def save_task(self,new_task, due_date, due_time):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO tasks (task, due_date, due_time) VALUES (?, ?, ?)", (new_task, due_date, due_time))
            print(f"Task '{new_task}' saved successfully.")
        except Exception as e:
            print(f"Error saving task: {e}")

    def delete_task_from_db(self,task, due_date, due_time):
        with self.conn:
            print(f"Executing DELETE FROM tasks WHERE task = '{task}' AND due_date = '{due_date}' AND due_time = '{due_time}'")  # Debug print
            self.conn.execute("DELETE FROM tasks WHERE task = ? AND due_date = ? AND due_time = ?", (task, due_date, due_time))
            self.conn.commit()  # Ensure the deletion is committed

    def schedule_notification(self,task, due_date, due_time):
        due_datetime_str = f"{due_date} {due_time}"
        due_datetime = datetime.strptime(due_datetime_str, "%Y-%m-%d %H:%M")
        delay = (due_datetime - datetime.now()).total_seconds()

        if delay > 0:
            threading.Timer(delay, self.show_notification, args=(task,)).start()
            print(f"Scheduled notification for task '{task}' at {due_datetime_str}")


    def update_task_count_label(self):
        self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

    def load_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT task, due_date, due_time FROM tasks")
            tasks = cursor.fetchall()
            for task_info in tasks:
                task, due_date, due_time = task_info
                # Add task to your application logic here
                print(f"Loaded task: {task} due on {due_date} at {due_time}")
                self.add_task_to_study_list(task, due_date, due_time, from_db=True)  # Call add_task_to_study_list with from_db=True
        except Exception as e:
            print(f"Error loading tasks: {e}")


if __name__ == "__main__":
    root = Tk()
    app = MainInterface(root)
    root.mainloop()
    pygame.quit()