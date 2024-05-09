import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

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

        self.scrollable_study_frame = ScrollableFrame(self, bg="light yellow")
        self.scrollable_study_frame.pack(padx=20,pady=10, fill=tk.BOTH, expand=True)

        self.study_frame = self.scrollable_study_frame.scrollable_frame
 
        self.study_label = tk.Label(self.study_frame, text="To Do:", font=("Cooper Black", 30), bg="white")  
        self.study_label.pack(pady=5)

        self.task_widgets = []  # List to store task widgets (checkbutton, due date label, and delete button)
        self.task_count = 0  # Initialize task count to 0
        self.task_count_label = tk.Label(self.study_frame, text="Number of tasks: 0", font=("Times New Roman", 12), bg="white")
        self.task_count_label.pack(anchor="w", padx=20)

        # Button to delete all tasks
        self.delete_all_button = tk.Button(self, text="Delete All Task", command=self.delete_all_tasks, font=("Times New Roman", 15), width=15, height=1, bg="white", fg="black")
        self.delete_all_button.pack(pady=1, side=tk.BOTTOM)

    def select_due_date(self):
        top = tk.Toplevel(self)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', font=('Times New Roman', 10), bg="light yellow")  
        cal.pack(pady=20, fill="both", expand=True)
        confirm_button = tk.Button(top, text="Confirm", command=lambda: self.confirm_due_date(cal, top), font=("Times New Roman", 10), bg="light yellow")  
        confirm_button.pack(pady=5)

    def confirm_due_date(self, cal, top):
        self.selected_date = cal.get_date()
        top.destroy()

    def add_task(self):
        new_task = self.new_task_entry.get()
        if new_task and self.selected_date:
            # Checkbutton for the new task
            task_checkbutton = tk.Checkbutton(self.study_frame, text=new_task, font=("Times New Roman", 20), bg="white")
            task_checkbutton.pack(anchor="w")
            task_checkbutton.var = tk.BooleanVar()  # BooleanVar to track the state of the checkbox
            task_checkbutton.config(variable=task_checkbutton.var, command=lambda: self.mark_completed(task_checkbutton))

            # Frame to hold the due date label with a box around it
            due_date_frame = tk.Frame(self.study_frame, bd=1, relief=tk.SOLID, bg="white")
            due_date_frame.pack(anchor="w", padx=20, pady=(0,5))
            due_date_label = tk.Label(due_date_frame, text=f"Due: {self.selected_date}", font=("Times New Roman", 8), bg="white")
            due_date_label.pack(padx=5, pady=2)
            
            # Button to delete the task
            delete_button = tk.Button(self.study_frame, text="❌", command=lambda: self.delete_task(task_checkbutton, due_date_frame, delete_button), bg="light yellow")
            delete_button.pack(anchor="e")

            # Pack both task widgets (checkbutton, due date label, and delete button) into a tuple and store in task_widgets list
            self.task_widgets.append((task_checkbutton, due_date_frame, delete_button))
            self.task_count += 1  # Increment task count
            self.update_task_count_label()  # Update task count label
            
            self.new_task_entry.delete(0, "end")
            self.selected_date = None
        else:
            messagebox.showwarning("Warning", "Please enter a task and select its due date.")
    
    def mark_completed(self, checkbutton):
        if checkbutton.var.get():
            checkbutton.config(fg="gray")  # Change text color to gray when task is completed
            self.task_count -= 1  # Decrement task count
        else:
            checkbutton.config(fg="black")  # Change text color back to black when task is incomplete
            self.task_count += 1  # Increment task count
        self.update_task_count_label()  # Update task count label

    def delete_task(self, task_checkbutton, due_date_frame, delete_button):
        task_checkbutton.destroy()  # Destroy the checkbutton
        due_date_frame.destroy()  # Destroy the due date frame
        delete_button.destroy()  # Destroy the delete button
        self.task_widgets.remove((task_checkbutton, due_date_frame, delete_button))  # Remove task from task_widgets list
        self.task_count -= 1  # Decrement task count
        self.update_task_count_label()  # Update task count label

    def delete_all_tasks(self):
        for widget_tuple in self.task_widgets:
            widget_tuple[0].destroy()  # Destroy the checkbutton
            widget_tuple[1].destroy()  # Destroy the due date frame
            widget_tuple[2].destroy()  # Destroy the delete button
        self.task_widgets = []  # Clear the list of task widgets
        self.task_count = 0
        self.update_task_count_label()

    def update_task_count_label(self):
        self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

# Create an instance of the StudyListApp class
app = StudyListApp()
# Start the tkinter event loop
app.mainloop()
