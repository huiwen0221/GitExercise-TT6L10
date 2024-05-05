from tkinter import *
import time
import winsound

class MainInterface:
    def __init__(self,root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "IndianRed")

        #Defining Grid 
        self.root.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
        self.root.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight = 1, uniform='a')

        def user_data():
            pass
        
        def badges_user():
            pass

        def calendar_user():
            pass

        def studylist_user():
            pass

        def switch_default_mode():
            root.config(bg="IndianRed")
            hide_frames()
            self.timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)

            self.default_timer_btn.grid(row = 1, column = 4, columnspan =2 , sticky="nsew")
            self.default_start_btn.grid(row =9 , column =0, columnspan =2, sticky="nsew" )
            self.default_stop_btn.grid(row =9 , column =2 , columnspan =2, sticky="nsew" )
            self.default_reset_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.default_shortbreak_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )
            self.default_longbreak_btn.grid(row =9 , column =8 , columnspan =2, sticky="nsew")

        def study_mode():
            root.config(bg="Cornflowerblue")
            hide_frames()

            self.study_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)
            self.study_timer_btn.grid(row = 1, column = 4, columnspan =2 , sticky="nsew")
            self.study_start_btn.grid(row =9 , column =0, columnspan =2, sticky="nsew" )
            self.study_stop_btn.grid(row =9 , column =2 , columnspan =2, sticky="nsew" )
            self.study_reset_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.study_shortbreak_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )
            self.study_longbreak_btn.grid(row =9 , column =8 , columnspan =2, sticky="nsew")
        
        def relax_mode():
            root.config(bg="mediumseagreen")
            hide_frames()

            self.relax_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)
            self.relax_timer_btn.grid(row = 1, column = 4, columnspan =2 , sticky="nsew")
            self.relax_start_btn.grid(row =9 , column =0, columnspan =2, sticky="nsew" )
            self.relax_stop_btn.grid(row =9 , column =2 , columnspan =2, sticky="nsew" )
            self.relax_reset_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" ) 
            self.relax_shortbreak_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )
            self.relax_longbreak_btn.grid(row =9 , column =8 , columnspan =2, sticky="nsew")

        def hide_frames():
            self.timer_lbl.grid_forget()
            self.default_timer_btn.grid_forget()
            self.default_start_btn.grid_forget()
            self.default_stop_btn.grid_forget()
            self.default_reset_btn.grid_forget()
            self.default_shortbreak_btn.grid_forget()
            self.default_longbreak_btn.grid_forget()

            self.study_timer_lbl.grid_forget()
            self.study_timer_btn.grid_forget()
            self.study_start_btn.grid_forget()
            self.study_stop_btn.grid_forget()
            self.study_reset_btn.grid_forget()
            self.study_shortbreak_btn.grid_forget()
            self.study_longbreak_btn.grid_forget()

            self.relax_timer_lbl.grid_forget()
            self.relax_timer_btn.grid_forget()
            self.relax_start_btn.grid_forget()
            self.relax_stop_btn.grid_forget()
            self.relax_reset_btn.grid_forget()
            self.relax_shortbreak_btn.grid_forget()
            self.relax_longbreak_btn.grid_forget()

        #Menu Taskbar
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

     #User Menu (Statistics, Achievements, Calendar, Study List)
        user_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Statistics", command=user_data)
        user_menu.add_command(label="Achievements", command=badges_user)
        user_menu.add_separator()
        user_menu.add_command(label="Calendar", command=calendar_user)
        user_menu.add_command(label="Study List", command=studylist_user)

    #Mode Menu (Default, Study, Relax)
        mode_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Default Mode", command=switch_default_mode)
        mode_menu.add_command(label="Study Mode", command=study_mode)
        mode_menu.add_command(label="Relax Mode", command=relax_mode)

    #Settings Menu (Timer, Template, Sounds, Notification System)
        setting_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Settings",menu=setting_menu)

        setting_menu.add_command(label="Open")

    #Create buttons and label for Default Mode
        self.timer_lbl = Label(root, text = "25:00", font= ("Times", 100,), fg ="black", bg = "IndianRed")

        self.default_timer_btn = Button(text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey",command =self.defaultmode_timer )
        self.default_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_default_time)
        self.default_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_default_time)
        self.default_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_default_time)
        self.default_shortbreak_btn = Button(text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.defaultmode_shortbreak)
        self.default_longbreak_btn = Button(text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.defaultmode_longbreak)

    #Create Study Mode Buttons and Label
        self.study_timer_lbl = Label(root, text = "45:00", font= ("Times", 100,), fg ="black", bg = "cornflowerblue")

        self.study_timer_btn = Button(text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey",command =self.studymode_timer)
        self.study_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_study_time)
        self.study_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_study_time)
        self.study_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_study_time)
        self.study_shortbreak_btn = Button(text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.studymode_shortbreak)
        self.study_longbreak_btn = Button(text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.studymode_longbreak)

    #Relax Mode Label and Buttons
        self.relax_timer_lbl = Label(root, text = "15:00", font= ("Times", 100,), fg ="black", bg = "mediumseagreen")

        self.relax_timer_btn = Button(text = "Timer", font=("Times, 16"), fg = "black",activebackground = "grey",command =self.relaxmode_timer)
        self.relax_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_relax_time)
        self.relax_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_relax_time)
        self.relax_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_relax_time)
        self.relax_shortbreak_btn = Button(text = "Short Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.relaxmode_shortbreak)
        self.relax_longbreak_btn = Button(text = "Long Break", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.relaxmode_longbreak)

        switch_default_mode()
    # Default mode timer variables
        self.default_run_timer = False
        self.default_start_timer = 0
        self.default_pause_timer = False
        self.default_timer_duration = 1500
        self.default_remaining_time = self.default_timer_duration

        # Study mode timer variables
        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration

        # Relax mode timer variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration

##DEFAULT
    def defaultmode_timer(self): #25 mins
        self.default_timer_duration = 1500
        self.default_remaining_time = self.default_timer_duration
        self.reset_default_time()

    def defaultmode_shortbreak(self): #5 mins
        self.default_timer_duration = 300
        self.default_remaining_time = self.default_timer_duration
        self.reset_default_time()

    def defaultmode_longbreak(self): #15 mins
        self.default_timer_duration = 900
        self.default_remaining_time = self.default_timer_duration
        self.reset_default_time()

##STUDY
    def studymode_timer(self): #45 mins
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.reset_study_time()

    def studymode_shortbreak(self): #15 mins
        self.study_timer_duration = 900
        self.study_remaining_time = self.study_timer_duration
        self.reset_study_time()

    def studymode_longbreak(self): #25 mins
        self.study_timer_duration = 1500
        self.study_remaining_time = self.study_timer_duration
        self.reset_study_time()

##RELAX
    def relaxmode_timer(self): #15 mins
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.reset_relax_time()          

    def relaxmode_shortbreak(self): #20 mins
        self.relax_timer_duration = 1200
        self.relax_remaining_time = self.relax_timer_duration
        self.reset_relax_time()

    def relaxmode_longbreak(self): #30 mins
        self.relax_timer_duration = 1800
        self.relax_remaining_time = self.relax_timer_duration
        self.reset_relax_time()

# Default mode timer functions
    def start_default_time(self):
        if not self.default_run_timer:
            self.default_run_timer = True
            self.default_start_timer = time.time()
            self.update_default_time()

    def pause_default_time(self):
        if self.default_run_timer:
            self.default_run_timer = False

    def reset_default_time(self):
        self.default_run_timer = False
        self.default_remaining_time = self.default_timer_duration
        self.update_default_display()

    def update_default_time(self):
        if self.default_run_timer:
            current_time = time.time()
            time_passed = current_time - self.default_start_timer
            self.default_remaining_time = max(self.default_remaining_time - time_passed, 0)
            self.update_default_display()

            if self.default_remaining_time > 0:
                self.default_start_timer = current_time
                self.root.after(1000, self.update_default_time)
            else:
                self.default_run_timer = False
                self.alarm_sound()

    def update_default_display(self):
        minutes = int(self.default_remaining_time // 60)
        seconds = int(self.default_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

#Default Alarm Sound 
    def alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME, winsound.SND_ASYNC)



##Study Mode BUTTON FUNCTIONALITY
    def start_study_time(self):
        if not self.study_run_timer:
            self.study_run_timer = True
            self.study_start_timer = time.time()
            self.update_study_time()

    def pause_study_time(self):
        if self.study_run_timer:
            self.study_run_timer = False

    def reset_study_time(self):
        self.study_run_timer = False
        self.study_remaining_time = self.study_timer_duration
        self.update_study_display()

    def update_study_time(self):
        if self.study_run_timer:
            current_time = time.time()
            time_passed = current_time - self.study_start_timer
            self.study_remaining_time = max(self.study_remaining_time - time_passed, 0)
            self.update_study_display()

            if self.study_remaining_time > 0:
                self.study_start_timer = current_time
                self.root.after(1000, self.update_study_time)
            else:
                self.study_run_timer = False
                self.alarm_sound()

    def update_study_display(self):
        minutes = int(self.study_remaining_time // 60)
        seconds = int(self.study_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.study_timer_lbl.config(text=time_str)



    # Relax mode timer functions
    def start_relax_time(self):
        if not self.relax_run_timer:
            self.relax_run_timer = True
            self.relax_start_timer = time.time()
            self.update_relax_time()

    def pause_relax_time(self):
        if self.relax_run_timer:
            self.relax_run_timer = False

    def reset_relax_time(self):
        self.relax_run_timer = False
        self.relax_remaining_time = self.relax_timer_duration
        self.update_relax_display()

    def update_relax_time(self):
        if self.relax_run_timer:
            current_time = time.time()
            time_passed = current_time - self.relax_start_timer
            self.relax_remaining_time = max(self.relax_remaining_time - time_passed, 0)
            self.update_relax_display()

            if self.relax_remaining_time > 0:
                self.relax_start_timer = current_time
                self.root.after(1000, self.update_relax_time)
            else:
                self.relax_run_timer = False
                self.alarm_sound()

    def update_relax_display(self):
        minutes = int(self.relax_remaining_time // 60)
        seconds = int(self.relax_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.relax_timer_lbl.config(text=time_str)

if __name__ == "__main__":
    root = Tk()
    app = MainInterface(root)
    root.mainloop()