from tkinter import *
import time
import winsound

root = Tk()

#Setting up Window's size and design by defining Class
class RelaxTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "mediumseagreen")

#Bottom Buttons Frame
        self.relax_bottom_frame = Frame(root, bg="mediumseagreen", height=50)
        self.relax_bottom_frame.pack(side=BOTTOM, fill=X)
        
#Top Buttons Frame
        self.relax_top_bar_frame = Frame(root, bg="mediumseagreen")
        self.relax_top_bar_frame.pack(fill=X)

#Timer Label Design [CENTRE]
        self.relax_timer_lbl = Label(root, text = "15:00", font= ("Times", 78,), fg ="black", bg = "mediumseagreen")
        self.relax_timer_lbl.pack(pady=20)
        self.relax_timer_lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

#Study Mode Timer Button [TOP CENTRE]
        self.relax_timer_btn = Button(self.relax_top_bar_frame, text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey", command=self.relax_default_timer )
        self.relax_timer_btn.pack(side=TOP, padx=5, pady=10, anchor=CENTER)

#Start Button Design [BOTTOM]
        self.relax_start_btn = Button(self.relax_bottom_frame,text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.relax_start_time)
        self.relax_start_btn.pack(side=LEFT, expand=True, fill=X)

#Stop Button Design [BOTTOM]
        self.relax_stop_btn = Button(self.relax_bottom_frame, text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.relax_pause_time)
        self.relax_stop_btn.pack(side=LEFT, expand=True, fill=X)

#Reset Button Design [BOTTOM]
        self.relax_reset_btn = Button(self.relax_bottom_frame, text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.relax_reset_time)
        self.relax_reset_btn.pack(side=LEFT, expand=True, fill=X)

#Short Break Button Design [BOTTOM]
        self.relax_shortbreak_btn = Button(self.relax_bottom_frame, text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.relax_short_break )
        self.relax_shortbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Long Break Button Design [BOTTOM]
        self.relax_longbreak_btn = Button(self.relax_bottom_frame, text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.relax_long_break)
        self.relax_longbreak_btn.pack(side=LEFT, expand=True, fill=X)

#Timer Variables (Original State)
        self.relax_run_timer = FALSE #Timer not running
        self.relax_start_timer = 0 #Initialized to 0
        self.relax_pause_timer = FALSE #Timer isn't paused
        self.relax_timer_duration = 900 #15mins * 60 seconds = 900 seconds
        self.relax_remaining_time = self.relax_timer_duration #set as same value to show that entire duration is remaining

#Default Timer Mode
    def relax_default_timer(self):
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_reset_time()

#Short Break
    def relax_short_break(self):
        self.relax_timer_duration = 600
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_reset_time()

#Long Break
    def relax_long_break(self):
        self.relax_timer_duration = 1200
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_reset_time()

#Start Timer [ALL]
    def relax_start_time(self):
        if not self.relax_run_timer: #if the timer is not running,
            self.relax_run_timer = TRUE #change the timer to run.
            self.relax_start_timer = time.time()
            self.relax_update_time()
            self.relax_start_btn.configure(state = DISABLED)
            self.relax_stop_btn.configure(state= NORMAL)

#Pause Timer [ALL]
    def relax_pause_time(self):
        if self.relax_run_timer: #if timer is running,
            self.relax_run_timer = FALSE #change it to not run.
            self.relax_start_btn.configure(state = NORMAL)
            self.relax_stop_btn.configure(state = DISABLED)

#Reset Timer [ALL]
    def relax_reset_time(self):
        self.relax_run_timer = False
        self.relax_remaining_time = self.relax_timer_duration #resetting timer to initial duration
        self.relax_start_btn.configure(state = NORMAL)
        self.relax_stop_btn.configure(state = DISABLED)
        self.relax_update_display()

#Updating time inside
    def relax_update_time(self):
        if self.relax_run_timer: #if timer is running,
            relax_current_time = time.time() #get current time and find the time passed since it started
            relax_time_passed = relax_current_time - self.relax_start_timer
            self.relax_remaining_time = max(self.relax_remaining_time - relax_time_passed, 0) #prevents remaining time from become less than 0
            self.relax_update_display()

            if self.relax_remaining_time > 0:
                self.relax_start_timer = relax_current_time
                self.root.after(1000, self.relax_update_time) #1000 = 1 second, updates after 1 second
            else: 
                self.relax_run_timer = False
                self.relax_alarm_sound()

#Updating time outside and displaying it
    def relax_update_display(self):
        minutes = int(self.relax_remaining_time // 60)
        seconds = int(self.relax_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.relax_timer_lbl.config(text=time_str)

#Default Alarm Sound 
    def relax_alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME, winsound.SND_ASYNC)
            

relax_timer = RelaxTimer(root)
root.mainloop()