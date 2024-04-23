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

    def confirm_due_date(self, cal, top):
        self.selected_date = cal.get_date()
        top.destroy()

    def add_task(self):
        new_task = self.new_task_entry.get()
        if new_task and self.selected_date:
            # Create a Checkbutton for the new task
            task_checkbutton = tk.Checkbutton(self.study_frame, text=new_task, font=("Times New Roman", 20), bg="white")
            task_checkbutton.pack(anchor="w")
            task_checkbutton.var = tk.BooleanVar()  # Create a BooleanVar to track the state of the checkbox
            task_checkbutton.config(variable=task_checkbutton.var, command=lambda: self.mark_completed(task_checkbutton))

            # Create a frame to hold the due date label with a box around it
            due_date_frame = tk.Frame(self.study_frame, bd=1, relief=tk.SOLID, bg="white")
            due_date_frame.pack(anchor="w", padx=20, pady=(0,5))
            due_date_label = tk.Label(due_date_frame, text=f"Due: {self.selected_date}", font=("Times New Roman", 8), bg="white")
            due_date_label.pack(padx=5, pady=2)
            
            # Pack both task widget (checkbutton and due date label) into a tuple and store in task_widgets list
            self.task_widgets.append((task_checkbutton, due_date_frame))
            self.task_count += 1  # Increment task count
            self.update_task_count_label()  # Update task count label
            
            self.new_task_entry.delete(0, "end")
            self.selected_date = None
        else:
            messagebox.showwarning("Warning", "Please enter a task and select its due date.")
    
    def mark_completed(self, checkbutton):
        if checkbutton.var.get():
            checkbutton.config(fg="gray")  # Change text color to gray when task is completed
            
            # Remove the task checkbutton and its due date label from the GUI
            for widget_tuple in self.task_widgets:
                if widget_tuple[0] == checkbutton:  # Find the tuple containing the checkbutton
                    checkbutton.destroy()
                    widget_tuple[1].destroy()  # Destroy the associated due date frame
                    self.task_widgets.remove(widget_tuple)  # Remove the tuple from the list
                    self.task_count -= 1  # Decrement task count
                    self.update_task_count_label()  # Update task count label
                    break
        else:
            checkbutton.config(fg="black")  # Change text color back to black when task is incomplete

    def update_task_count_label(self):
        self.task_count_label.config(text=f"Number of tasks: {self.task_count}")

# Create an instance of the StudyListApp class
app = StudyListApp()
# Start the tkinter event loop
app.mainloop()