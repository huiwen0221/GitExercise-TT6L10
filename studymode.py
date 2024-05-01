from tkinter import *
import time
import winsound

root = Tk()

#Setting up Window's size and design by defining Class
class StudyTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "cornflowerblue")

#Bottom Buttons Frame
        self.frame = Frame(root, bg="cornflowerblue", height=50)
        self.frame.pack(side=BOTTOM, fill=X)
        
#Top Buttons Frame
        self.top_bar_frame = Frame(root, bg="cornflowerblue")
        self.top_bar_frame.pack(fill=X)

#Timer Label Design [CENTRE]
        self.timer_lbl = Label(root, text = "45:00", font= ("Times", 78,), fg ="black", bg = "cornflowerblue")
        self.timer_lbl.pack(pady=20)
        self.timer_lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

#Default Mode Timer Button [TOP CENTRE]
        self.default_btn = Button(self.top_bar_frame, text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey", command=self.default_timer )
        self.default_btn.pack(side=TOP, padx=5, pady=10, anchor=CENTER)

#Start Button Design [BOTTOM]
        self.start_btn = Button(self.frame,text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.start_time)
        self.start_btn.pack(side=LEFT, expand=True, fill=X)

#Stop Button Design [BOTTOM]
        self.stop_btn = Button(self.frame, text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.pause_time)
        self.stop_btn.pack(side=LEFT, expand=True, fill=X)

#Reset Button Design [BOTTOM]
        self.reset_btn = Button(self.frame, text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.reset_time)
        self.reset_btn.pack(side=LEFT, expand=True, fill=X)

#Short Break Button Design [BOTTOM]
        self.shortbreak_btn = Button(self.frame, text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.short_break )
        self.shortbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Long Break Button Design [BOTTOM]
        self.longbreak_btn = Button(self.frame, text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.long_break)
        self.longbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Timer Variables (Original State)
        self.run_timer = FALSE #Timer not running
        self.start_timer = 0 #Initialized to 0
        self.pause_timer = FALSE #Timer isn't paused
        self.timer_duration = 2700 #25mins * 60 seconds = 1500 seconds
        self.remaining_time = self.timer_duration #set as same value to show that entire duration is remaining

#Default Timer Mode
    def default_timer(self):
        self.timer_duration = 2700
        self.remaining_time = self.timer_duration
        self.reset_time()

#Short Break
    def short_break(self):
        self.timer_duration = 900
        self.remaining_time = self.timer_duration
        self.reset_time()

#Long Break
    def long_break(self):
        self.timer_duration = 1500
        self.remaining_time = self.timer_duration
        self.reset_time()

#Start Timer [ALL]
    def start_time(self):
        if not self.run_timer: #if the timer is not running,
            self.run_timer = TRUE #change the timer to run.
            self.start_timer = time.time()
            self.update_time()
            self.start_btn.configure(state = DISABLED)
            self.stop_btn.configure(state= NORMAL)

#Pause Timer [ALL]
    def pause_time(self):
        if self.run_timer: #if timer is running,
            self.run_timer = FALSE #change it to not run.
            self.start_btn.configure(state = NORMAL)
            self.stop_btn.configure(state = DISABLED)

#Reset Timer [ALL]
    def reset_time(self):
        self.run_timer = False
        self.remaining_time = self.timer_duration #resetting timer to initial duration
        self.start_btn.configure(state = NORMAL)
        self.stop_btn.configure(state = DISABLED)
        self.update_display()

#Updating time inside
    def update_time(self):
        if self.run_timer: #if timer is running,
            current_time = time.time() #get current time and find the time passed since it started
            time_passed = current_time - self.start_timer
            self.remaining_time = max(self.remaining_time - time_passed, 0) #prevents remaining time from become less than 0
            self.update_display()

            if self.remaining_time > 0:
                self.start_timer = current_time
                self.root.after(1000, self.update_time) #1000 = 1 second, updates after 1 second
            else: 
                self.run_timer = False
                self.alarm_sound()

#Updating time outside and displaying it
    def update_display(self):
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

#Default Alarm Sound 
    def alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME, winsound.SND_ASYNC)
            

study_timer = StudyTimer(root)
root.mainloop()