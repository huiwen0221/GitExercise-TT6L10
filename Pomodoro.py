from tkinter import *
import time
import winsound

root = Tk()

#Setting up Window's size and design by defining Class
class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "IndianRed")

        self.frame = Frame(root, bg="IndianRed", height=50)
        self.frame.pack(side=BOTTOM, fill=X)
        

        #Timer Label Design [CENTRE]
        self.timer_lbl = Label(root, text = "25:00", font= ("Times", 66,), fg ="black", bg = "IndianRed")
        self.timer_lbl.pack(pady=20)
        self.timer_lbl.place(relx=0.5, rely=0.4, anchor=CENTER)

        #Start Button Design
        self.start_btn = Button(self.frame,text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.start_time)
        self.start_btn.pack(side=LEFT, expand=True, fill=X)

        #Stop Button Design
        self.stop_btn = Button(self.frame, text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.pause_time)
        self.stop_btn.pack(side=LEFT, expand=True, fill=X)


        #Reset Button Design
        self.reset_btn = Button(self.frame, text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey", command=self.reset_time)
        self.reset_btn.pack(side=LEFT, expand=True, fill=X)

        #Timer Variables (Original State)
        self.run_timer = FALSE #Timer not running
        self.start_timer = 0 #Initialized to 0
        self.pause_timer = FALSE #Timer isn't paused
        self.timer_duration = 1500 #25mins * 60 seconds = 1500 seconds
        self.remaining_time = self.timer_duration

    def start_time(self):
        if not self.run_timer: #if the timer is not running,
            self.run_timer = TRUE #change the timer to run and follow logic below.
            self.start_timer = time.time()
            self.update_time()
            self.start_btn.configure(state = DISABLED)
            self.stop_btn.configure(state= NORMAL)
    

    def pause_time(self):
        if self.run_timer: #if timer is running,
            self.run_timer = FALSE #change it to not run.
            self.start_btn.configure(state = NORMAL)
            self.stop_btn.configure(state = DISABLED)
        
    def reset_time(self):
        self.run_timer = False
        self.remaining_time = self.timer_duration
        self.start_btn.configure(state = NORMAL)
        self.stop_btn.configure(state = DISABLED)
        self.update_display()


    def update_time(self):
        if self.run_timer:
            current_time = time.time()
            time_passed = current_time - self.start_timer
            self.remaining_time = max(self.remaining_time - time_passed, 0) #prevents remaining time from become less than 0
            self.update_display()

            if self.remaining_time > 0:
                self.start_timer = current_time
                self.root.after(1000, self.update_time) #1000 = 1 second
            else: #stop timer and play alarm sound
                self.run_timer = False
                self.alarm_sound()
    
    def update_display(self):
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

    #Default Alarm Sound 
    def alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME, winsound.SND_ASYNC)
            

pomodoro_timer = PomodoroTimer(root)
root.mainloop()