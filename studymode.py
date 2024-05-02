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
        self.study_bottom_frame = Frame(root, bg="cornflowerblue", height=50)
        self.study_bottom_frame.pack(side=BOTTOM, fill=X)
        
#Top Buttons Frame
        self.study_top_bar_frame = Frame(root, bg="cornflowerblue")
        self.study_top_bar_frame.pack(fill=X)

#Timer Label Design [CENTRE]
        self.study_timer_lbl = Label(root, text = "45:00", font= ("Times", 78,), fg ="black", bg = "cornflowerblue")
        self.study_timer_lbl.pack(pady=20)
        self.study_timer_lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

#Study Mode Timer Button [TOP CENTRE]
        self.study_timer_btn = Button(self.study_top_bar_frame, text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey", command=self.study_default_timer )
        self.study_timer_btn.pack(side=TOP, padx=5, pady=10, anchor=CENTER)

#Start Button Design [BOTTOM]
        self.study_start_btn = Button(self.study_bottom_frame,text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.study_start_time)
        self.study_start_btn.pack(side=LEFT, expand=True, fill=X)

#Stop Button Design [BOTTOM]
        self.study_stop_btn = Button(self.study_bottom_frame, text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.study_pause_time)
        self.study_stop_btn.pack(side=LEFT, expand=True, fill=X)

#Reset Button Design [BOTTOM]
        self.study_reset_btn = Button(self.study_bottom_frame, text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.study_reset_time)
        self.study_reset_btn.pack(side=LEFT, expand=True, fill=X)

#Short Break Button Design [BOTTOM]
        self.study_shortbreak_btn = Button(self.study_bottom_frame, text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.study_short_break )
        self.study_shortbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Long Break Button Design [BOTTOM]
        self.study_longbreak_btn = Button(self.study_bottom_frame, text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.study_long_break)
        self.study_longbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Timer Variables (Original State)
        self.study_run_timer = FALSE #Timer not running
        self.study_start_timer = 0 #Initialized to 0
        self.study_pause_timer = FALSE #Timer isn't paused
        self.study_timer_duration = 2700 #45mins * 60 seconds = 2700 seconds
        self.study_remaining_time = self.study_timer_duration #set as same value to show that entire duration is remaining

#Default Timer Mode
    def study_default_timer(self):
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_reset_time()

#Short Break
    def study_short_break(self):
        self.study_timer_duration = 900
        self.study_remaining_time = self.study_timer_duration
        self.study_reset_time()

#Long Break
    def study_long_break(self):
        self.study_timer_duration = 1500
        self.study_remaining_time = self.study_timer_duration
        self.study_reset_time()

#Start Timer [ALL]
    def study_start_time(self):
        if not self.study_run_timer: #if the timer is not running,
            self.study_run_timer = TRUE #change the timer to run.
            self.study_start_timer = time.time()
            self.study_update_time()
            self.study_start_btn.configure(state = DISABLED)
            self.study_stop_btn.configure(state= NORMAL)

#Pause Timer [ALL]
    def study_pause_time(self):
        if self.study_run_timer: #if timer is running,
            self.study_run_timer = FALSE #change it to not run.
            self.study_start_btn.configure(state = NORMAL)
            self.study_stop_btn.configure(state = DISABLED)

#Reset Timer [ALL]
    def study_reset_time(self):
        self.study_run_timer = False
        self.study_remaining_time = self.study_timer_duration #resetting timer to initial duration
        self.study_start_btn.configure(state = NORMAL)
        self.study_stop_btn.configure(state = DISABLED)
        self.study_update_display()

#Updating time inside
    def study_update_time(self):
        if self.study_run_timer: #if timer is running,
            study_current_time = time.time() #get current time and find the time passed since it started
            study_time_passed = study_current_time - self.study_start_timer
            self.study_remaining_time = max(self.study_remaining_time - study_time_passed, 0) #prevents remaining time from become less than 0
            self.study_update_display()

            if self.study_remaining_time > 0:
                self.study_start_timer = study_current_time
                self.root.after(1000, self.study_update_time) #1000 = 1 second, updates after 1 second
            else: 
                self.study_run_timer = False
                self.study_alarm_sound()

#Updating time outside and displaying it
    def study_update_display(self):
        minutes = int(self.study_remaining_time // 60)
        seconds = int(self.study_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.study_timer_lbl.config(text=time_str)

#Default Alarm Sound 
    def study_alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME, winsound.SND_ASYNC)
            

study_timer = StudyTimer(root)
root.mainloop()