from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from tkinter import messagebox, ttk


class CalendarTask:
    def __init__(self, root):
        self.root = root
        self.task = {}
        
        #Calendar frame
        self.mainframe = Frame(root, width=500, height=250)  
        self.mainframe.pack(side=RIGHT, pady=10, padx=10)
        self.mainframe.pack_propagate(False)
        

        #Calendar 
        self.calendar = Calendar(font="Arial 14", selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, width=15, height=10 )
        self.calendar.pack(pady=10, expand=False) 
        self.calendar.bind("<<CalendarSelected>>", self.date_selected)

        #Task frame
        self.task_frame = Frame(self.mainframe)
        self.task_frame.pack(fill=BOTH, expand=True)

        # Task entry widget
        self.task_entry = Entry(self.task_frame)
        self.task_entry.pack(side=LEFT,fill=X, padx=5)

        #Add task
        self.add_task_button = Button(self.task_frame, text="Add your task", command=self.addtask)
        self.add_task_button.pack(side=LEFT, pady=5)

        # Task list (Listbox)
        self.task_list = ttk.Treeview(self.mainframe, columns=("Date", "Task"), show="headings")
        self.task_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.task_list.heading("Date", text="Date")
        self.task_list.heading("Task", text="Task")
        
        #Time entry for notification
        self.hour_entry = ttk.Combobox(self.task_frame, values=[f"{hour:02d}" for hour in range(24)], width=3)
        self.hour_entry.pack(side=LEFT, padx=5)
        self.minute_entry = ttk.Combobox(self.task_frame, values=[f"{minute:02d}" for minute in range(60)], width=3)
        self.minute_entry.pack(side=LEFT, padx=5)

    def addtask(self): #to add task
        date = self.selected_date if hasattr(self, 'selected_date') else self.calendar.selection_get() #ensure
        task = self.task_entry.get()
        hour = self.hour_entry.get()
        minute = self.minute_entry.get()
        task_time = f"{hour}:{minute}"
        if task and hour and minute: #include time data in addtask
            task_info = {'task': task, 'time': task_time}
            if date in self.task:
                self.task[date].append(task_info)
            else:
                self.task[date] = [task_info]
            self.task_entry.delete(0,'end')
            messagebox.showinfo("Task added", "Task added successfully!")
            self.update_calendar_tasks()
            self.addtask_list()
        else:
         messagebox.showwarning("No Task", "Please enter a task and time.") 

    def update_calendar_tasks(self):
        for date in self.task:
           self.calendar.calevent_create(date, 'Task', 'task') #show user that the task is updated

    def date_selected(self,event): #shows task event when click on the date
        self.selected_date = self.calendar.selection_get()
        self.addtask_list()

    def addtask_list(self):
        self.task_list.delete(*self.task_list.get_children())
        for date, tasks in self.task.items():
            for task in tasks:
                self.task_list.insert("", END, values=(date.strftime('%Y-%m-%d'), task['task']))


if __name__ == "__main__":
    root = Tk()
    root.title("Calendar")
    app = CalendarTask(root)  
    root.mainloop()
        