from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime


class CalendarTask:
    def __init__(self, root):
        self.root = root
        self.task = {}
        
        #Calendar frame
        self.mainframe = Frame(root, width=300, height=250)  
        self.mainframe.pack(side=RIGHT, pady=10, padx=10)
        self.mainframe.pack_propagate(False)
        

        #Calendar 
        self.calendar = Calendar(font="Arial 14", selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day )
        self.calendar.pack(pady=10, fill=BOTH, expand=True) 
        self.calendar.bind("<<CalendarSelected>>", self.date_selected)

        #Task frame
        self.task_frame = Frame(self.mainframe)
        self.task_frame.pack(fill=X, expand=True)

        # Task entry widget
        self.task_entry = Entry(self.task_frame)
        self.task_entry.pack(side=LEFT,fill=X, padx=5)

        #Add task
        self.add_task_button = Button(self.task_frame, text="Add your task", command=self.addtask)
        self.add_task_button.pack(side=LEFT, pady=5)
        
    def addtask(self): #to add task
        date = self.selected_date if hasattr(self, 'selected_date') else self.calendar.selection_get() #ensure
        task = self.task_entry.get()
        if task:
            if date in self.task:
                self.task[date].append(task) #add multiple task
            else:
                self.task[date]=[task] #create a new list for another new date selected
                self.update_calendar_tasks()
                self.task_entry.delete(0, 'end') #clear input field to enter new task
                messagebox.showinfo("Task Added", "Task added successfully!") #notify the user 
        else:
         messagebox.showwarning("No Task", "Please enter a task.") 

    def update_calendar_tasks(self):
        for date in self.task:
           self.calendar.calevent_create(date, 'Task', 'task') #show user that the task is updated

    def date_selected(self,event): #shows task event when click on the date
        self.selected_date = self.calendar.selection_get()
        if self.selected_date in self.task:
            task_info = '\n'.join(self.task[self.selected_date]) 
            messagebox.showinfo("Tasks on " + str(self.selected_date), task_info)
        else: messagebox.showinfo("Tasks on " + str(self.selected_date),"No task on "+ str(self.selected_date))

if __name__ == "__main__":
    root = Tk()
    root.title("Calendar")
    app = CalendarTask(root)  
    root.mainloop()
        