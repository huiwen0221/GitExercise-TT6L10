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

