from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from tkinter import messagebox, ttk
import threading
import time
from notifypy import Notify


class CalendarTask:
    def __init__(self, root):
        self.root = root
        self.task = {}
        root.geometry("600x400") 
        root.config(bg="lightgrey")


        self.calendar = Calendar(font="Arial 14", selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, width=15, height=10 )
        self.calendar.grid(row=0, column=0,rowspan=5,columnspan=5,padx=10,pady=10,sticky="senw" )
        self.calendar.bind("<<CalendarSelected>>", self.date_selected)

        self.task_entry = Entry()
        self.task_entry.grid(row= 0,column=6,padx=10,pady=10,sticky="n")
        #Add task
        self.add_task_button = Button(text="Add your task", command=self.addtask)
        self.add_task_button.grid(row=0, column=7,padx=10, pady=10,sticky="n")

        # Task list (Listbox)
        self.task_list = ttk.Treeview(columns=("Date", "Time", "Task"), show="headings")
        self.task_list.grid(row=1, column=6, columnspan=9)
        self.task_list.heading("Date", text="Date")
        self.task_list.heading("Time", text="Time")
        self.task_list.heading("Task", text="Task")
                
        
        #Time entry for notification
        self.hour_entry = ttk.Combobox(values=[f"{hour:02d}" for hour in range(24)], width=3)
        self.hour_entry.grid(row=0,column=8,)
        self.minute_entry = ttk.Combobox(values=[f"{minute:02d}" for minute in range(60)], width=3)
        self.minute_entry.grid(row=0,column=9)
        self.start_notification_system()

    def addtask(self): #to add task
        date = self.selected_date if hasattr(self, 'selected_date') else self.calendar.selection_get()
        task = self.task_entry.get()
        hour = self.hour_entry.get()
        minute = self.minute_entry.get()
        if task and hour and minute:
            task_time = f"{hour}:{minute}"
            notify_time = datetime.strptime(f"{date} {task_time}", "%Y-%m-%d %H:%M")
            self.task[notify_time] = {'task': task, 'time': task_time}
            self.task_entry.delete(0, 'end')
            messagebox.showinfo("Task added", "Task added successfully!")
            self.addtask_list()
            self.addtask_list()

    def update_calendar_tasks(self):
        for date in self.task:
           self.calendar.calevent_create(date, 'Task', 'task') #show user that the task is updated

    def date_selected(self,event): #shows task event when click on the date
        self.selected_date = self.calendar.selection_get()
        self.addtask_list()

    def addtask_list(self):
        self.task_list.delete(*self.task_list.get_children())
        for notify_time, info in self.task.items():
            self.task_list.insert("", "end", values=(notify_time.strftime("%Y-%m-%d"), info['time'], info['task']))
    
    def start_notification_system(self):
        def checktasks():
            while True:
                now = datetime.now()
                to_remove = []
                for notify_time, task in self.tasks.items():
                    if now >= notify_time:
                        Notify().show_toast("Task Reminder", f"Time for your task: {task}", duration=10)
                        to_remove.append(notify_time)
                for time in to_remove:
                    del self.tasks[time]
                time.sleep(60)
        thread=threading.Thread(target=checktasks,daemon=True)
        thread.start


if __name__ == "__main__":
    root = Tk()
    root.title("Calendar")
    app = CalendarTask(root)  
    root.mainloop()
        