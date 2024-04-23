import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

class StudyListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study List")
        self.geometry("400x300")
        self.configure(bg="light yellow")
        
        self.title_label = tk.Label(self, text="Study List", font=("Cooper Black", 50), bg="light yellow")  
        self.title_label.pack(pady=10)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(padx=20, pady=30, fill=tk.X)

        self.new_task_entry = tk.Entry(self.entry_frame, font=("Times New Roman", 20), width=30)  
        self.new_task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.due_date_button = tk.Button(self.entry_frame, text="Select Due Date", command=self.select_due_date, font=("Times New Roman", 12), width=15, height=2, bg="white")  
        self.due_date_button.pack(side=tk.LEFT, padx=(5,0))

        self.add_button = tk.Button(self.entry_frame, text="Add", command=self.add_task, font=("Times New Roman", 12), width=15, height=2, bg="white")  
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.selected_date = None

        self.study_frame = tk.Frame(self, bg="white", bd=2, relief=tk.RIDGE, width=300)  
        self.study_frame.pack(padx=20,pady=10, fill=tk.BOTH, expand=True, anchor="n") 

        self.study_label = tk.Label(self.study_frame, text="T0D0:", font=("Cooper Black", 30), bg="white")  
        self.study_label.pack(pady=5)

        self.task_widgets = []  # List to store task widgets (checkbutton and due date label)
        self.task_count = 0  # Initialize task count to 0
        self.task_count_label = tk.Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 12), bg="white")
        self.task_count_label.pack(anchor="w", padx=20)

        def select_due_date(self):
           top = tk.Toplevel(self)
           cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', font=('Times New Roman', 10), bg="light yellow")  
           cal.pack(pady=20, fill="both", expand=True)
           confirm_button = tk.Button(top, text="Confirm", command=lambda: self.confirm_due_date(cal, top), font=("Times New Roman", 10), bg="light yellow")  
           confirm_button.pack(pady=5)