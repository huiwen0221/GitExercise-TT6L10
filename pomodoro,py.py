import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from plyer import notification
import threading
()

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg="white")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.delta < 0:  # Only scroll up when delta is negative
            self.canvas.yview_scroll(-1*(event.delta//200), "units")  # Invert direction

class StudyListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study List")
        self.geometry("600x600")
        self.configure(bg="light yellow")

        self.calendar_button = tk.Button(self, text="Calendar", command=self.open_calendar, font=("Times New Roman", 10), width=10, height=1, bg="white")
        self.calendar_button.place(x=10, y=10)  # Use place() method for absolute positioning  

        self.title_label = tk.Label(self, text="Study List", font=("Cooper Black", 50), bg="light yellow")  
        self.title_label.pack(pady=10)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)

        self.new_task_entry = tk.Entry(self.entry_frame, font=("Times New Roman", 20), width=30)  
        self.new_task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.due_date_button = tk.Button(self.entry_frame, text="Select Due Date", command=self.select_due_date, font=("Times New Roman", 12), width=15, height=2, bg="white")  
        self.due_date_button.pack(side=tk.LEFT, padx=(5,0))

        self.due_time_button = tk.Button(self.entry_frame, text="Select Due Time", command=self.select_time, font=("Times New Roman", 12), width=15, height=2, bg="white")  
        self.due_time_button.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.entry_frame, text="Add", command=self.add_task, font=("Times New Roman", 12), width=15, height=2, bg="white")  
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.selected_date = None
        self.selected_time = None  # Initialize selected_time variable

        self.scrollable_study_frame = ScrollableFrame(self, bg="light yellow")
        self.scrollable_study_frame.pack(padx=20,pady=10, fill=tk.BOTH, expand=True)

        self.study_frame = self.scrollable_study_frame.scrollable_frame

        self.study_label = tk.Label(self.study_frame, text="To Do:", font=("Cooper Black", 30), bg="white")  
        self.study_label.pack(pady=5)

        self.task_widgets = []  # List to store task widgets (checkbutton, due date label, and delete button)
        self.task_count = 0  # Initialize task count to 0
        self.task_count_label = tk.Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 10), bg="white")
        self.task_count_label.pack(anchor="w", padx=20)

        # Button to delete all tasks
        self.delete_all_button = tk.Button(self, text="Delete All Task", command=self.delete_all_tasks, font=("Times New Roman", 10), width=15, height=1, bg="white", fg="black")
        self.delete_all_button.pack(pady=1, side=tk.BOTTOM)

        self.calendar_tasks = {}  # Dictionary to store tasks associated with each date on the calendar

        # Initialize the SQLite database
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()
        self.load_tasks()
    

       
    def create_table(self):
       with self.conn:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                due_date TEXT NOT NULL,
                due_time TEXT NOT NULL
            )
        """)


    def load_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT task, due_date ,due_time FROM tasks")
        tasks = cursor.fetchall()
        for task, due_date, due_time in tasks:
            self.add_task_to_study_list(task, due_date, due_time)
            self.update_calendar(task, due_date, due_time)  # Add tasks to calendar

    def select_due_date(self):
        top = tk.Toplevel(self)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', font=('Times New Roman', 10),bg="light yellow") 
        cal.pack(pady=20, fill="both", expand=True)
        confirm_button = tk.Button(top, text="Confirm", command=lambda: self.confirm_due_date(cal, top), font=("Times New Roman", 10), bg="light yellow")  
        confirm_button.pack(pady=5)

    def confirm_due_date(self, cal, top):
        self.selected_date = cal.get_date()
        top.destroy()

    def select_time(self):
        top = tk.Toplevel(self)
        top.title("Select Time")
        top.geometry("200x150")

        hour_label = tk.Label(top, text="Hour (0-23):", font=("Times New Roman", 10))
        hour_label.pack(pady=5)
        hour_entry = tk.Entry(top, font=("Times New Roman", 10))
        hour_entry.pack(pady=5)

        minute_label = tk.Label(top, text="Minute (0-59):", font=("Times New Roman", 10))
        minute_label.pack(pady=5)
        minute_entry = tk.Entry(top, font=("Times New Roman", 10))
        minute_entry.pack(pady=5)

        confirm_button = tk.Button(top, text="Confirm", font=("Times New Roman", 10),command=lambda: self.confirm_time(hour_entry.get(), minute_entry.get(), top))
        confirm_button.pack(pady=5)

    def confirm_time(self, hour, minute, top):
        try:
            hour = int(hour)
            minute = int(minute)
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.selected_time = f"{hour:02}:{minute:02}"
                top.destroy()
            else:
                messagebox.showwarning("Invalid Time", "Please enter a valid time.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter numeric values for hour and minute.")
    
    def add_task(self):
        new_task = self.new_task_entry.get()
        if new_task and self.selected_date and self.selected_time:
          # Add task to study list
         self.add_task_to_study_list(new_task, self.selected_date, self.selected_time)

        # Add task to calendar
         self.update_calendar(new_task, self.selected_date, self.selected_time)

        # Save task to database
         self.save_task(new_task, self.selected_date, self.selected_time)

        # Update calendar frame
         self.update_calendar_frame()

         self.new_task_entry.delete(0, "end")
         self.selected_date = None
         self.selected_time = None

        else:
         messagebox.showwarning("Warning", "Please enter a task, select its due date, and set the time.")


    def save_task(self, task, due_date, due_time):
        with self.conn:
            self.conn.execute("INSERT INTO tasks (task, due_date, due_time) VALUES (?, ?, ?)", (task, due_date, due_time))
            self.conn.commit()

    def add_task_to_study_list(self, new_task, due_date, due_time):
    # Checkbutton for the new task
       task_checkbutton = tk.Checkbutton(self.study_frame, text=new_task, font=("Times New Roman", 20), bg="white")
       task_checkbutton.pack(anchor="w", pady=(5, 0))  # Adjust vertical padding

       task_checkbutton.var = tk.BooleanVar()
       task_checkbutton.config(variable=task_checkbutton.var, command=lambda: self.mark_completed(task_checkbutton, due_date))

    # Frame to hold the due date and due time labels
       due_info_frame = tk.Frame(self.study_frame, bg="light yellow")
       due_info_frame.pack(anchor="w", padx=20, pady=(0, 5), fill=tk.X)  # Ensure it stretches horizontally

    # Frame to hold both due date and due time labels in the same box
       due_date_time_frame = tk.Frame(due_info_frame, bd=1, relief=tk.SOLID, bg="light yellow")
       due_date_time_frame.pack(side="left", padx=5)

    # Due date label
       due_date_label = tk.Label(due_date_time_frame, text=f"Due Date: {due_date}", font=("Times New Roman", 10), bg="light yellow")
       due_date_label.pack(padx=5, pady=2)

    # Due time label
       due_time_label = tk.Label(due_date_time_frame, text=f"Due Time: {due_time}", font=("Times New Roman", 10), bg="light yellow")
       due_time_label.pack(padx=5, pady=2)

    # Button to delete the task
       delete_button = tk.Button(self.study_frame, text="❌", command=lambda: self.delete_task(task_checkbutton, due_info_frame, delete_button), bg="light yellow")
       delete_button.pack(anchor="e", pady=(5, 0))  # Adjust vertical padding

    # Pack both task widgets (checkbutton, due info frame, and delete button) into a tuple and store in task_widgets list
       self.task_widgets.append((task_checkbutton, due_info_frame, delete_button, new_task, due_date, due_time))
       self.task_count += 1  # Increment task count
       self.update_task_count_label()  # Update task count label

       self.schedule_notification(new_task, due_date, due_time)

    def mark_completed(self, checkbutton, due_date, due_time):
        if checkbutton.var.get():
            checkbutton.config(fg="gray")  # Change text color to gray when task is completed
            self.task_count -= 1  # Decrement task count
            
            # Remove the task from the calendar_tasks dictionary
            task_text = checkbutton.cget("text")
            if due_date in self.calendar_tasks and task_text in self.calendar_tasks[due_date,due_time]:
                self.calendar_tasks[due_date,due_time].remove(task_text)
                if not self.calendar_tasks[due_date,due_time]:
                    del self.calendar_tasks[due_date,due_time]
            
            # Update the calendar frame
            self.update_calendar_frame()
            
            # Remove task from database
            self.delete_task_from_db(task_text, due_date,due_time)
            
            # Remove task from the study list
            self.delete_task(checkbutton, None, None)
            
        else:
            checkbutton.config(fg="black")  # Change text color back to black when task is incomplete
            self.task_count += 1  # Increment task count
            self.update_task_count_label()  # Update task count label

    def delete_task(self, task_checkbutton, due_info_frame, delete_button):
        # Extract stored task text, due date, and due time
        task_info = next((task_info for task_cb, due_date_time_frame, delete_button, *task_info in self.task_widgets if task_cb == task_checkbutton), None)

        if task_info:
            task_text, due_date, due_time = task_info

            print(f"Deleting task: '{task_text}', due date: '{due_date}', due time: '{due_time}'")  # Debug print

            task_checkbutton.destroy()  # Destroy the checkbutton
            due_info_frame.destroy()  # Destroy the due date frame
            delete_button.destroy()  # Destroy the delete button

            self.task_widgets = [(task_cb, due_frame, del_btn, *task_info) for task_cb, due_frame, del_btn, *task_info in self.task_widgets if task_cb != task_checkbutton]
            self.task_count -= 1  # Decrement task count
            self.update_task_count_label()  # Update task count label

            # Remove task from database
            self.delete_task_from_db(task_text, due_date, due_time)

    def delete_task_from_db(self, task, due_date, due_time):
        with self.conn:
            print(f"Executing DELETE FROM tasks WHERE task = '{task}' AND due_date = '{due_date}' AND due_time = '{due_time}'")  # Debug print
            self.conn.execute("DELETE FROM tasks WHERE task = ? AND due_date = ? AND due_time = ?", (task, due_date, due_time))
            self.conn.commit()  # Ensure the deletion is committed

    def delete_all_tasks(self):
            for widget_tuple in self.task_widgets:
                widget_tuple[0].destroy()  # Destroy the checkbutton
                widget_tuple[1].destroy()  # Destroy the due date frame
                widget_tuple[2].destroy()  # Destroy the delete button
            self.task_widgets = []  # Clear the list of task widgets
            self.task_count = 0
            self.update_task_count_label()

            # Remove all tasks from database
            with self.conn:
                self.conn.execute("DELETE FROM tasks")

        # Update the calendar frame if it's open
            self.update_calendar_frame()

    def update_task_count_label(self):
        self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

    def update_calendar(self, task, due_date ,due_time):
        # Add the task to the dictionary of calendar tasks
        if due_date not in self.calendar_tasks:
            self.calendar_tasks[due_date] = []
        self.calendar_tasks[due_date].append((task, due_time))  #Store task along with due time as a tuple
        print(f"Added task '{task}' with due time '{due_time}' to date {due_date}. Current tasks for this date: {self.calendar_tasks[due_date]}")  #Debug print

    def open_calendar(self):
        # Close previous calendar window if exists
        if hasattr(self, "calendar_window"):
            self.calendar_window.destroy()

        # Create a top-level window for the calendar
        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.title("Calendar")
        self.calendar_window.geometry("600x400")  # Set the size of the Toplevel window

        # Create a frame to contain the calendar widget
        calendar_frame = tk.Frame(self.calendar_window, bg="light yellow")
        calendar_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

        # Create the calendar widget
        self.calendar = Calendar(calendar_frame, font="Arial 14", selectmode='day')
        self.calendar.pack(fill="both", expand=True)

        # Bind a function to handle date selection on the calendar
        self.calendar.bind("<<CalendarSelected>>", lambda event: self.display_calendar_tasks(event, self.calendar, self.calendar_window))

        # Frame to display the tasks for the selected date
        self.task_frame = tk.Frame(self.calendar_window, bg="light yellow", width=50)  # Fixed width for smaller size
        self.task_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill="both", expand=True)

        # Update the calendar frame to reflect current tasks
        self.update_calendar_frame()

    def display_calendar_tasks(self, calendar):
        # Get the selected date from the calendar
        selected_date = datetime.strptime(calendar.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")

        # Get tasks associated with the selected date
        tasks = self.calendar_tasks.get(selected_date, [])

        # Debug print
        print(f"Displaying tasks for {selected_date}: {tasks}")

        # Clear existing tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Create a label to show the selected date
        date_label = tk.Label(self.task_frame, text=f"Tasks for {selected_date}", font=("Arial", 14), bg="light yellow")
        date_label.pack(pady=10)

        # Display tasks associated with the selected date
        for task in tasks:
            task_label = tk.Label(self.task_frame, text=task, font=("Arial", 12), bg="light yellow")
            task_label.pack(pady=5)

    def update_calendar_frame(self):
        # Get the currently selected date from the calendar
        if hasattr(self, "calendar"):
            selected_date = datetime.strptime(self.calendar.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")
        
            # Get tasks associated with the selected date
            tasks = self.calendar_tasks.get(selected_date, [])

            # Debug print
            print(f"Updating calendar frame for {selected_date}: {tasks}")

            # Clear existing tasks
            for widget in self.task_frame.winfo_children():
                widget.destroy()

            # Create a label to show the selected date
            date_label = tk.Label(self.task_frame, text=f"Tasks for {selected_date}", font=("Arial", 14), bg="light yellow")
            date_label.grid(row=0, column=0, columnspan=2, pady=10)

            # Display tasks associated with the selected date
            for i, task in enumerate(tasks, start=1):
                task_label = tk.Label(self.task_frame, text=task, font=("Arial", 12), bg="light yellow")
                task_label.grid(row=i, column=0, sticky="w", padx=10, pady=5)


    def schedule_notification(self, task, due_date, due_time):
        due_datetime_str = f"{due_date} {due_time}"
        due_datetime = datetime.strptime(due_datetime_str, "%Y-%m-%d %H:%M")
        delay = (due_datetime - datetime.now()).total_seconds()
        
        if delay > 0:
            threading.Timer(delay, self.show_notification, args=(task,)).start()
            print(f"Scheduled notification for task '{task}' at {due_datetime_str}")

    def show_notification(self, task):
        notification.notify(
            title="Task Due",
            message=f"The task '{task}' is due now!",
            timeout=10
        )
        print(f"Notification shown for task '{task}'")

app = StudyListApp()
# Start the tkinter event loop
app.mainloop()