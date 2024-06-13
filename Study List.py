import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import customtkinter
from datetime import datetime

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

self = customtkinter.CTk()

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
        self.configure(bg="light blue")

        # Adjustments for calendar_button
        self.calendar_button = customtkinter.CTkButton(self, text="Calendar", command=self.open_calendar, bg_color=("light blue", "blue"))
        self.calendar_button.place(x=10, y=10)

        # Adjustments for title_label
        self.title_label = customtkinter.CTkLabel(self, text="Study List", font=("Cooper Black", 50), bg_color="light blue")
        self.title_label.pack(pady=10)

        # Adjustments for entry_frame
        self.entry_frame = customtkinter.CTkFrame(self, bg_color="light blue")
        self.entry_frame.pack(padx=20, pady=20, fill=tk.X)

       # Adjustments for new_task_entry
        self.new_task_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Add Your Task", height=50, width=200, font=("Times New Roman", 20), corner_radius=50, fg_color=("white", "blue"), bg_color="light blue")  
        self.new_task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Adjustments for due_date_button
        self.due_date_button = customtkinter.CTkButton(self.entry_frame, text="Select Due Date", height=50, width=100, command=self.select_due_date, font=("Times New Roman", 15), bg_color="light blue") 
        self.due_date_button.pack(side=tk.LEFT, padx=(5,0))

       # Adjustments for due_time_button
        self.due_time_button = customtkinter.CTkButton(self.entry_frame, text="Select Due Time", command=self.select_time, height=50, width=100, font=("Times New Roman", 15), bg_color="light blue")  
        self.due_time_button.pack(side=tk.LEFT, padx=5)

        # Adjustments for add_button
        self.add_button = customtkinter.CTkButton(self.entry_frame, text="Add", command=self.add_task, height=50, width=100, font=("Times New Roman", 15), bg_color="light blue")  
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.selected_date = None
        self.selected_time = None  # Initialize selected_time variable

        self.scrollable_study_frame = ScrollableFrame(self, bg="light blue")
        self.scrollable_study_frame.pack(padx=20,pady=10, fill=tk.BOTH, expand=True)

        self.study_frame = self.scrollable_study_frame.scrollable_frame

        self.study_label = tk.Label(self.study_frame, text="To Do:", font=("Cooper Black", 30), bg="white")  
        self.study_label.pack(pady=5)

        self.task_widgets = []  # List to store task widgets (checkbutton, due date label, and delete button)
        self.task_count = 0  # Initialize task count to 0
        self.task_count_label = tk.Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 10), bg="white")
        self.task_count_label.pack(anchor="w", padx=20)

        # Button to delete all tasks
        self.delete_all_button = customtkinter.CTkButton(self, text="Delete All Task", command=self.delete_all_tasks, font=("Times New Roman", 10), height=30, width=100, bg_color="light yellow")  
        self.add_button.pack(side=tk.LEFT, padx=5)
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
                due_time TEXT  -- Add this line for due_time column
            )
        """)


    def load_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT task, due_date FROM tasks")
        tasks = cursor.fetchall()
        for task, due_date, due_time in tasks:
            self.add_task_to_study_list(task, due_date,due_time)
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
        try:
          with self.conn:
            print(f"Saving task: {task}, Due Date: {due_date}, Due Time: {due_time}")
            self.conn.execute("INSERT INTO tasks (task, due_date, due_time) VALUES (?, ?, ?)", (task, due_date, due_time))
            self.conn.commit()  # Commit the transaction to save changes
            print("Task saved successfully.")
        except sqlite3.Error as e:
           print(f"Error occurred: {e}")

    def add_task_to_study_list(self, new_task, due_date, due_time):
    # Checkbutton for the new task
       task_checkbutton = tk.Checkbutton(self.study_frame, text=new_task, font=("Times New Roman", 20), bg="white")
       task_checkbutton.pack(anchor="w", pady=(5, 0))  # Adjust vertical padding

       task_checkbutton.var = tk.BooleanVar()
       task_checkbutton.config(variable=task_checkbutton.var, command=lambda: self.mark_completed(task_checkbutton, due_date))

    # Frame to hold the due date and due time labels
       due_info_frame = tk.Frame(self.study_frame, bg="white")
       due_info_frame.pack(anchor="w", padx=20, pady=(0, 5), fill=tk.X)  # Ensure it stretches horizontally

    # Frame to hold both due date and due time labels in the same box
       due_date_time_frame = tk.Frame(due_info_frame, bd=1, relief=tk.SOLID, bg="white")
       due_date_time_frame.pack(side="left", padx=5)

    # Due date label
       due_date_label = tk.Label(due_date_time_frame, text=f"Due Date: {due_date}", font=("Times New Roman", 10), bg="white")
       due_date_label.pack(padx=5, pady=2)

    # Due time label
       due_time_label = tk.Label(due_date_time_frame, text=f"Due Time: {due_time}", font=("Times New Roman", 10), bg="white")
       due_time_label.pack(padx=5, pady=2)

    # Pack both task widgets (checkbutton, due info frame, and delete button) into a tuple and store in task_widgets list
       self.task_widgets.append((task_checkbutton, due_info_frame))
       self.task_count += 1  # Increment task count
       self.update_task_count_label()  # Update task count label

    def mark_completed(self, checkbutton, due_date, due_time):
     if checkbutton.var.get():
        # Change text color to gray when task is completed
        checkbutton.config(fg="gray")

        # Remove the task from the calendar_tasks dictionary
        task_text = checkbutton.cget("text")
        for widget_tuple in self.task_widgets:
            if widget_tuple[0] == checkbutton:
                due_info_frame = widget_tuple[1]
                due_time_label = due_info_frame.winfo_children()[1]  # Assuming due time label is the second child
                due_time = due_time_label.cget("text").replace("Due Time: ", "")
                break

        if due_date in self.calendar_tasks and (task_text, due_time) in self.calendar_tasks[due_date]:
            self.calendar_tasks[due_date].remove((task_text, due_time))
            if not self.calendar_tasks[due_date]:
                del self.calendar_tasks[due_date]

        # Update the calendar frame
        self.update_calendar_frame()

        # Disable the checkbutton to prevent unchecking
        checkbutton.config(state="disabled")
        
        # Decrement task count only if it's not already completed
        if checkbutton["fg"] != "gray":
            self.task_count -= 1
            self.update_task_count_label()

        # Remove task from database
        self.delete_task_from_db(task_text, due_date, due_time)
        
     else:
        # Handle the case where the user attempts to uncheck a completed task
        # For example, show a message to the user that the task is already completed
        messagebox.showinfo("Task Completed", "This task has already been completed and cannot be unchecked.")


    
    def delete_task(self, task_checkbutton, due_date_frame, delete_button):
        # Extract task text and due date before destroying the widgets
        task_text = task_checkbutton.cget("text")
        due_date_text = due_date_frame.winfo_children()[0].cget("text").replace("Due: ", "") if due_date_frame else None
        
        # Destroy the widgets
        task_checkbutton.destroy()
        if due_date_frame:
            due_date_frame.destroy()
        if delete_button:
            delete_button.destroy()

        # Remove task from the task_widgets list
        for widget_tuple in self.task_widgets:
            if widget_tuple[0] == task_checkbutton:
                self.task_widgets.remove(widget_tuple)
                break
        self.task_count -= 1
        self.update_task_count_label()

        if task_text and due_date_text:
            self.delete_task_from_db(task_text,due_date_text)

        # Debug prints to check values
        print(f"Deleting task '{task_text}' with due date '{due_date_text}' from database.")

        # Remove task from the calendar_tasks dictionary
        if due_date_text in self.calendar_tasks:
            if task_text in self.calendar_tasks[due_date_text]:
                self.calendar_tasks[due_date_text].remove(task_text)
                if not self.calendar_tasks[due_date_text]:
                    del self.calendar_tasks[due_date_text]  # Remove the key if no tasks left for that date

        # Update the calendar frame if it's open
        self.update_calendar_frame()

    def delete_task_from_db(self, task, due_date):
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE task = ? AND due_date = ?", (task, due_date))
            # Ensure changes are committed
            self.conn.commit()
        # Debug print to confirm deletion
        print(f"Deleted task '{task}' with due date '{due_date}' from database.")

    def delete_all_tasks(self):
        for widget_tuple in self.task_widgets:
            widget_tuple[0].destroy()  # Destroy the checkbutton
            widget_tuple[1].destroy()  # Destroy the due date frame
            widget_tuple[2].destroy()  # Destroy the delete button
        self.task_widgets = []  # Clear the list of task widgets
        self.task_count = 0
        self.update_task_count_label()

        # Remove all tasks from calendar_tasks dictionary
        self.calendar_tasks.clear()

        # Remove all tasks from database
        with self.conn:
            self.conn.execute("DELETE FROM tasks")
            self.conn.commit()

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

    def display_calendar_tasks(self, event, calendar, calendar_window):
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

app = StudyListApp()
# Start the tkinter event loop
app.mainloop()