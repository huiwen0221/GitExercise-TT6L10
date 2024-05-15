from tkinter import *
import time
import winsound
from PomodoroSessions import insert_pomodoro_session

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

#Change to Default Mode
        def switch_default_mode():
            root.config(bg="IndianRed")
            hide_frames()
            self.timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)
            self.cycles_lbl.grid(row=0, column=4, columnspan = 2)

            self.default_start_btn.grid(row =9 , column =2, columnspan =2, sticky="nsew" )
            self.default_stop_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.default_reset_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )


#Change to Study Mode
        def study_mode():
            root.config(bg="Cornflowerblue")
            hide_frames()

            self.study_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)

            self.study_start_btn.grid(row =9 , column =2, columnspan =2, sticky="nsew" )
            self.study_stop_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.study_reset_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )


#Change to Relax Mode
        def relax_mode():
            root.config(bg="mediumseagreen")
            hide_frames()

            self.relax_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)

            self.relax_start_btn.grid(row =9 , column =2, columnspan =2, sticky="nsew" )
            self.relax_stop_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.relax_reset_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" ) 

#Hide other mode buttons when switching mode
        def hide_frames():
            self.timer_lbl.grid_forget()
 
            self.default_start_btn.grid_forget()
            self.default_stop_btn.grid_forget()
            self.default_reset_btn.grid_forget()
            self.cycles_lbl.grid_forget()

            self.study_timer_lbl.grid_forget()

            self.study_start_btn.grid_forget()
            self.study_stop_btn.grid_forget()
            self.study_reset_btn.grid_forget()

            self.relax_timer_lbl.grid_forget()

            self.relax_start_btn.grid_forget()
            self.relax_stop_btn.grid_forget()
            self.relax_reset_btn.grid_forget()
 

#Save Button Functionality
        def save_settings():
            timer_minutes = int(self.timer_entry.get() or 0)  #entry for timer
            timer_seconds = int(self.timerseconds_entry.get() or 0)
            shortbreak_minutes = int(self.shortbreak_entry.get() or 0) #entry for short break
            shortbreak_seconds = int(self.shortbreakseconds_entry.get() or 0)
            longbreak_minutes = int(self.longbreak_entry.get() or 0) #entry for long break
            longbreak_seconds = int(self.longbreakseconds_entry.get() or 0)
            repeat_cycles = int(self.repeat_cycles_entry.get() or 0) #entry for number of repeated cycles

            timer_duration = timer_minutes *60 + timer_seconds
            shortbreak_duration = shortbreak_minutes *60 + shortbreak_seconds
            longbreak_duration = longbreak_minutes *60 + longbreak_seconds


            self.default_timer_duration = timer_duration
            self.default_remaining_time = timer_duration

            self.default_shortbreak_duration = shortbreak_duration
            self.default_longbreak_duration = longbreak_duration

            self.number_cycles = repeat_cycles
            
            self.update_default_display()
            self.cycles_lbl.config(text="Cycles: {}".format(repeat_cycles))

#Reset All Entry Boxes and Revert to Original Default Mode
        def reset_default_mode():
            self.default_remaining_time = 1500
            self.default_shortbreak_duration = 300
            self.default_longbreak_duration = 900
            self.update_default_display()

            self.number_cycles= 0
            self.update_cycle_count_label()
            self.cycles_lbl.config(text="Cycles: 0")

            self.timer_entry.delete(0,END)
            self.timer_entry.insert(0,"25")
            self.timerseconds_entry.delete(0, END)
            self.timerseconds_entry.insert(0,"00")
            self.shortbreak_entry.delete(0,END)
            self.shortbreak_entry.insert(0,"5")
            self.shortbreakseconds_entry.delete(0,END)
            self.shortbreakseconds_entry.insert(0,"00")
            self.longbreak_entry.delete(0,END)
            self.longbreak_entry.insert(0,"15")
            self.longbreakseconds_entry.delete(0,END)
            self.longbreakseconds_entry.insert(0,"00")
            self.repeat_cycles_entry.delete(0,END)

#Settings Window
        def open_settings():
            settings_window = Toplevel(root)
            settings_window.title("Settings")
            settings_window.geometry("500x500")
            settings_window.configure(bg ="gray")

            settings_window.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
            settings_window.rowconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform='a')

        #Timer Settings Button
            self.timer_settings_btn = Button(settings_window, text="Timer", font=("Times", 25), fg="black",activebackground="gray")
            self.timer_settings_btn.grid(row = 0, column=0, sticky="nwes")

        #Timer Entry
            self.timer_entry_lbl= Label(settings_window, text="Timer Duration (minutes):(seconds)", font=("Arial",18), bg="gray", fg="black")
            self.timer_entry_lbl.grid(row = 0, column=1,columnspan=3)
            self.timer_entry = Entry(settings_window)
            self.timer_entry.grid(row = 0, column=4, columnspan=2, padx=10, pady=5)
            self.timer_entry.insert(0,"25")

            self.timerseconds_entry = Entry(settings_window)
            self.timerseconds_entry.grid(row = 0, column =7, columnspan =2, padx=10, pady=5)
            self.timerseconds_entry.insert(0,"00")

        #Short Break Entry
            self.shortbreak_entry_lbl= Label(settings_window, text="Short Break Duration (minutes):", font=("Arial",18), bg="gray", fg="black")
            self.shortbreak_entry_lbl.grid(row = 1, column=1, columnspan=3)
            self.shortbreak_entry = Entry(settings_window)
            self.shortbreak_entry.grid(row = 1, column=4, columnspan=2, padx=10, pady=5)
            self.shortbreak_entry.insert(0,"5")

            self.shortbreakseconds_entry = Entry(settings_window)
            self.shortbreakseconds_entry.grid(row = 1, column = 7, columnspan=2, padx=10, pady=5)
            self.shortbreakseconds_entry.insert(0, "00")

        #Long Break Entry
            self.longbreak_entry_lbl= Label(settings_window, text="Long Break Duration (minutes):", font=("Arial",18), bg="gray", fg="black")
            self.longbreak_entry_lbl.grid(row = 2, column=1, columnspan=3)
            self.longbreak_entry = Entry(settings_window)
            self.longbreak_entry.grid(row = 2, column=4, columnspan=2, padx=10, pady=5)
            self.longbreak_entry.insert(0,"15")

            self.longbreakseconds_entry = Entry(settings_window)
            self.longbreakseconds_entry.grid(row = 2, column=7, columnspan=2, padx=10, pady=5)
            self.longbreakseconds_entry.insert(0, "00")

        #Repeat Cycles Entry
            self.repeat_cycles_lbl= Label(settings_window, text="Number of Cycles to Repeat:", font=("Arial",18), bg="gray", fg="black")
            self.repeat_cycles_lbl.grid(row = 3, column=1, columnspan=3)
            self.repeat_cycles_entry = Entry(settings_window)
            self.repeat_cycles_entry.grid(row = 3, column=4, columnspan=2, padx=10, pady=5)


        #SAVE Settings
            self.save_btn=Button(settings_window, text="Save", font=("Arial",25), bg="white", fg="black", command=save_settings)
            self.save_btn.grid(row=9,column=4,columnspan=2,sticky="nsew")

        #RESET Settings Button
            self.reset_all_btn=Button(settings_window, text="RESET TO ORIGINAL", font=("Arial",15), bg="red", fg="black", activebackground="red", command=reset_default_mode)
            self.reset_all_btn.grid(row=9,column=9,columnspan=2,sticky="nsew")


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

    #Settings Menu(Open new settings window)
        setting_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Settings",menu=setting_menu)

        setting_menu.add_command(label="Open", command=open_settings)

    #Default Mode Buttons and Label
        self.timer_lbl = Label(root, text = "25:00", font= ("Times", 100,), fg ="black", bg = "IndianRed")
        self.cycles_lbl = Label(root, text="Cycles:", font=("Times", 16), fg="black", bg="IndianRed")


        self.default_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_default_time)
        self.default_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_default_time)
        self.default_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_default_time)

    #Study Mode Buttons and Label
        self.study_timer_lbl = Label(root, text = "45:00", font= ("Times", 100,), fg ="black", bg = "cornflowerblue")

        self.study_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_study_time)
        self.study_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_study_time)
        self.study_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_study_time)
    
    #Relax Mode Label and Buttons
        self.relax_timer_lbl = Label(root, text = "15:00", font= ("Times", 100,), fg ="black", bg = "mediumseagreen")
 
        self.relax_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_relax_time)
        self.relax_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_relax_time)
        self.relax_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_relax_time)

        switch_default_mode()

###########################################################################################################
#DEFAULT#

# Default mode timer variables
        self.default_run_timer = False
        self.default_start_timer = 0
        self.default_pause_timer = False
        self.default_timer_duration = 5
        self.default_remaining_time = self.default_timer_duration
        self.default_shortbreak_duration = 10  # Default short break duration in seconds
        self.default_longbreak_duration = 15   # Default long break duration in seconds

        self.timer_type = "default_timer"

        self.number_cycles = 0  # Initialize number of cycles to zero
        self.current_cycle = 0  #Current cycles is zero
        self.update_cycle_count_label()


    def defaultmode_timer(self): #25 mins
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "default_timer"
        self.start_default_time()

    def defaultmode_shortbreak(self): #5 mins
        self.default_timer_duration = self.default_shortbreak_duration
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "short_break"
        self.start_default_time()

    def defaultmode_longbreak(self): #15 mins
        self.default_timer_duration = self.default_longbreak_duration
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "long_break"
        self.start_default_time()

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
        if self.timer_type == "default_timer":
            self.default_remaining_time = self.default_timer_duration
        elif self.timer_type == "short_break":
            self.default_remaining_time = self.default_shortbreak_duration
        else:
            self.default_remaining_time = self.default_longbreak_duration
        self.update_default_display()

    def start_cycle(self):
        if self.number_cycles > 0:
            if self.current_cycle == 0:  # Timer phase
                self.default_run_timer = True
                self.default_start_timer = time.time()
                self.update_default_time()
            elif self.current_cycle == 1:  # Short break phase
                self.default_run_timer = False
                self.defaultmode_shortbreak()
            elif self.current_cycle == 2:  # Long break phase
                self.default_run_timer = False
                self.defaultmode_longbreak()
                self.current_cycle = 0  # Reset cycle for the next round
                self.number_cycles -= 1
                self.update_cycle_count_label()
                
                if self.number_cycles > 0:
                    self.start_cycle()
                    self.number_cycles -= 1
                    self.update_cycle_count_label()

        else:
            # Handle case when no cycles left
            self.number_cycles = 0
            self.current_cycle = 0
            self.update_cycle_count_label()

    #Updating the number of cycles label as it completes each round
    def update_cycle_count_label(self):
        self.cycles_lbl.config(text="Cycles: {}".format(self.number_cycles))

    #Updating the timer, and the number of cycles each time it completes
    def update_default_time(self):
        if self.default_run_timer:
            current_time = time.time() #get current time and find the time passed since it started
            time_passed = current_time - self.default_start_timer  #
            self.default_remaining_time = max(self.default_remaining_time - time_passed, 0)#prevents remaining time from become less than 0
            self.update_default_display()

            if self.default_remaining_time > 0:
                self.default_start_timer = current_time
                self.root.after(1000, self.update_default_time)
            else:
                # Timer has ended
                self.default_run_timer = False
                self.alarm_sound()

                if self.timer_type == "default_timer":
                    # Switch to short break
                    self.timer_type = "short_break"
                    self.default_remaining_time = self.default_shortbreak_duration
                elif self.timer_type == "short_break":
                    # Switch to long break
                    self.timer_type = "long_break"
                    self.default_remaining_time = self.default_longbreak_duration
                else:
                    # Switch back to study timer
                    self.timer_type = "default_timer"
                    self.default_remaining_time = self.default_timer_duration
                    # Don't start the timer automatically, wait for user input

                # Update the display with the new timer type and remaining time
                self.update_default_display()
                # Automatically start the next timer (short break or long break), unless it's a study timer
                if self.timer_type != "default_timer":
                    self.start_default_time()
                else:
                    # Start a new cycle
                    self.start_cycle()

    def update_default_display(self):
        minutes = int(self.default_remaining_time // 60)
        seconds = int(self.default_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

#################################################################################################################
#STUDY#

# Study mode timer variables
        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_shortbreak_duration = 900
        self.study_longbreak_duration = 1500

        self.study_type = "study_timer"


##STUDY MODE
    def studymode_timer(self): #45 mins
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_timer"

    def studymode_shortbreak(self): #15 mins
        self.study_timer_duration = self.study_shortbreak_duration
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_shortbreak"

    def studymode_longbreak(self): #25 mins
        self.study_timer_duration = self.study_longbreak_duration
        self.study_remaining_time = self.study_timer_duration
        self.start_study_time()
        self.study_type = "study_longbreak"

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
        if self.study_type == "study_timer":
            self.study_remaining_time = self.study_timer_duration
        elif self.study_type == "study_shortbreak":
            self.study_remaining_time = self.study_shortbreak_duration
        else:
            self.default_remaining_time = self.study_longbreak_duration
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

                if self.study_type == "study_timer":
                    # Switch to short break
                    self.study_type = "study_shortbreak"
                    self.study_remaining_time = self.study_shortbreak_duration
                elif self.study_type == "study_shortbreak":
                    # Switch to long break
                    self.study_type = "study_longbreak"
                    self.default_remaining_time = self.study_longbreak_duration
                else:
                    # Switch back to study timer
                    self.study_type = "study_timer"
                    self.study_remaining_time = self.study_timer_duration
                    # Don't start the timer automatically, wait for user input
                    return

                # Update the display with the new timer type and remaining time
                self.update_study_display()
                # Automatically start the next timer (short break or long break), unless it's a study timer
                if self.study_type != "study_timer":
                    self.start_study_time()

    def update_study_display(self):
        minutes = int(self.study_remaining_time // 60)
        seconds = int(self.study_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.study_timer_lbl.config(text=time_str)

#########################################################################################################33
#RELAX#
        # Relax mode timer variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_shortbreak_duration = 1200
        self.relax_longbreak_duration = 1800

        self.relax_type = "relax_timer"

##RELAX
    def relaxmode_timer(self): #15 mins
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_timer"          

    def relaxmode_shortbreak(self): #20 mins
        self.relax_timer_duration = self.relax_shortbreak_duration
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_shortbreak"  

    def relaxmode_longbreak(self): #30 mins
        self.relax_timer_duration = self.relax_longbreak_duration
        self.relax_remaining_time = self.relax_timer_duration
        self.start_relax_time()
        self.relax_type = "relax_longbreak"  

##Relax mode timer functions
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
        if self.relax_type == "study_timer":
            self.relax_remaining_time = self.relax_timer_duration
        elif self.relax_type == "study_shortbreak":
            self.relax_remaining_time = self.relax_shortbreak_duration
        else:
            self.relax_remaining_time = self.relax_longbreak_duration
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

                if self.relax_type == "relax_timer":
                    # Switch to short break
                    self.relax_type = "relax_shortbreak"
                    self.relax_remaining_time = self.relax_shortbreak_duration
                elif self.relax_type == "relax_shortbreak":
                    # Switch to long break
                    self.relax_type = "relax_longbreak"
                    self.relax_remaining_time = self.relax_longbreak_duration
                else:
                    # Switch back to study timer
                    self.relax_type = "relax_timer"
                    self.relax_remaining_time = self.relax_timer_duration
                    # Don't start the timer automatically, wait for user input
                    return

                # Update the display with the new timer type and remaining time
                self.update_relax_display()
                # Automatically start the next timer (short break or long break), unless it's a study timer
                if self.relax_type != "relax_timer":
                    self.start_relax_time()

    def update_relax_display(self):
        minutes = int(self.relax_remaining_time // 60)
        seconds = int(self.relax_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.relax_timer_lbl.config(text=time_str)


#Default Alarm Sound 
    def alarm_sound(self):
        winsound.PlaySound("default-timer-sound.wav", winsound.SND_FILENAME)

    def complete_pomodoro_session(self, mode, timer_duration, short_break_duration, long_break_duration):
        # Insert the completed timer session into the database
        insert_pomodoro_session(mode, 'Timer', timer_duration)
        insert_pomodoro_session(mode, 'Short Break', short_break_duration)
        insert_pomodoro_session(mode, 'Long Break', long_break_duration)


if __name__ == "__main__":
    root = Tk()
    app = MainInterface(root)
    root.mainloop()