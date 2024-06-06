from tkinter import *
import time
import sqlite3
from datetime import datetime
from tkinter import ttk
from tkinter import colorchooser
import pygame



class MainInterface:
    def __init__(self,root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "IndianRed")

        pygame.init()
        pygame.mixer.init()

        #Defining Grid 
        self.root.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
        self.root.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight = 1, uniform='a')

        # Create database for Pomodoro
        self.conn = sqlite3.connect('pomodorohelper.db')
        self.cursor = self.conn.cursor()

        # Create Table if not exists
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PomodoroSessions (
            SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
            User TEXT NOT NULL,
            Mode TEXT NOT NULL,
            SessionType TEXT NOT NULL,
            Duration INTEGER NOT NULL,
            CompletionTime TEXT NOT NULL
        );""")

        # Create Table for User Settings if not exists
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UserSettings (
            SettingID INTEGER PRIMARY KEY AUTOINCREMENT,
            TimerDuration INTEGER NOT NULL,
            ShortBreakDuration INTEGER NOT NULL,
            LongBreakDuration INTEGER NOT NULL,
            RepeatCycles INTEGER NOT NULL,
            TimerEndSound TEXT NOT NULL,
            ShortBreakSound TEXT NOT NULL,
            LongBreakSound TEXT NOT NULL,
            BackgroundColor TEXT NOT NULL,
            Volume INTEGER NOT NULL
        );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Presets (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TimerDuration INTEGER,
            ShortBreakDuration INTEGER,
            LongBreakDuration INTEGER,
            RepeatCycles INTEGER,
            TimerEndSound TEXT,
            ShortBreakSound TEXT,
            LongBreakSound TEXT,
            BackgroundColor TEXT,
            Volume INTEGER
        );""")

        self.sound_files = {
            "Default Alarm": "Default Timer Alarm.wav",
            "Referee Whistle": "Study Referee Alarm.wav",
            "Chime": "Relax Chime Alarm.wav",
            "Default Short Break": "Default SB.wav",
            "Churchbell": "Study Churchbell SB.wav",
            "Wind Chimes": "Relax WindChimes SB.wav",
            "Default Microwave": "Default Microwave LB.wav",
            "Great Harp": "Study Great Harp LB.wav",
            "Relaxing Harp": "Relax Harp LB.wav"
        }

        self.timer_end_sound = self.sound_files["Default Alarm"]
        self.short_break_sound = self.sound_files["Default Short Break"]
        self.long_break_sound = self.sound_files["Default Microwave"]
        self.background_color="Indianred"

        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_shortbreak_duration = 900
        self.study_longbreak_duration = 1500

        self.volume = 50
        self.study_type = "study_timer"
        self.study_cycle_count = 0

################
        # Relax mode timer variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_shortbreak_duration = 1200
        self.relax_longbreak_duration = 1800

        self.relax_type = "relax_timer"
        self.relax_cycle_count = 0

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
            self.session_type_lbl.grid(row=2, column=2, columnspan=6)

#Change to Study Mode
        def study_mode():
            root.config(bg="Cornflowerblue")
            hide_frames()

            self.study_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)

            self.study_start_btn.grid(row =9 , column =2, columnspan =2, sticky="nsew" )
            self.study_stop_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.study_reset_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" )
            self.study_session_type_lbl.grid(row=2, column=2, columnspan=6)

#Change to Relax Mode
        def relax_mode():
            root.config(bg="mediumseagreen")
            hide_frames()

            self.relax_timer_lbl.grid(row=1,column=2,rowspan=6,columnspan=6,)

            self.relax_start_btn.grid(row =9 , column =2, columnspan =2, sticky="nsew" )
            self.relax_stop_btn.grid(row =9 , column =4 , columnspan =2, sticky="nsew" )
            self.relax_reset_btn.grid(row =9 , column =6 , columnspan =2, sticky="nsew" ) 
            self.relax_session_type_lbl.grid(row=2, column=2, columnspan=6)

#Hide other mode buttons when switching mode
        def hide_frames():
            self.timer_lbl.grid_forget()
 
            self.default_start_btn.grid_forget()
            self.default_stop_btn.grid_forget()
            self.default_reset_btn.grid_forget()
            self.cycles_lbl.grid_forget()
            self.session_type_lbl.grid_forget()

            self.study_timer_lbl.grid_forget()

            self.study_start_btn.grid_forget()
            self.study_stop_btn.grid_forget()
            self.study_reset_btn.grid_forget()
            self.study_session_type_lbl.grid_forget()

            self.relax_timer_lbl.grid_forget()

            self.relax_start_btn.grid_forget()
            self.relax_stop_btn.grid_forget()
            self.relax_reset_btn.grid_forget()
            self.relax_session_type_lbl.grid_forget()

        def open_color():
            # Open color picker dialog
            color = colorchooser.askcolor(title="Choose Color")
            new_bg_color = None  # Default value
            if color[1]:  # If a color is selected
                new_bg_color = color[1]  # Get the hexadecimal color code
            # Update background color of specified elements
            root.configure(bg=new_bg_color)
            self.timer_lbl.configure(bg=new_bg_color)
            self.cycles_lbl.configure(bg=new_bg_color)
            self.session_type_lbl.configure(bg=new_bg_color)
            self.background_color = new_bg_color

        def update_volume(val):
            volume = int(val) / 100  # Scale to 0-1 for pygame
            pygame.mixer.music.set_volume(volume)
            self.volume_label.config(text=f"Volume: {val}%")

        def save_preset1_settings():
            save_preset_settings(1)

        def save_preset2_settings():
            save_preset_settings(2)

        def save_preset3_settings():
            save_preset_settings(3)

        def load_preset1_settings():
            load_preset_settings(1)

        def load_preset2_settings():
            load_preset_settings(2)

        def load_preset3_settings():
            load_preset_settings(3)

        def save_preset_settings(preset_number):
            # Retrieve settings from UI inputs
            timer_minutes = int(self.timer_entry.get() or 0)
            timer_seconds = int(self.timerseconds_entry.get() or 0)
            shortbreak_minutes = int(self.shortbreak_entry.get() or 0)
            shortbreak_seconds = int(self.shortbreakseconds_entry.get() or 0)
            longbreak_minutes = int(self.longbreak_entry.get() or 0)
            longbreak_seconds = int(self.longbreakseconds_entry.get() or 0)
            repeat_cycles = int(self.repeat_cycles_entry.get() or 0)

            timer_duration = timer_minutes * 60 + timer_seconds
            shortbreak_duration = shortbreak_minutes * 60 + shortbreak_seconds
            longbreak_duration = longbreak_minutes * 60 + longbreak_seconds

            selected_timer_end_sound = self.alarm_sound_combobox.get()
            selected_short_break_sound = self.SB_sound_combobox.get()
            selected_long_break_sound = self.LB_sound_combobox.get()

            self.timer_end_sound = self.sound_files[selected_timer_end_sound]
            self.short_break_sound = self.sound_files[selected_short_break_sound]
            self.long_break_sound = self.sound_files[selected_long_break_sound]

            self.default_timer_duration = timer_duration
            self.default_remaining_time = timer_duration

            self.default_shortbreak_duration = shortbreak_duration
            self.default_longbreak_duration = longbreak_duration

            self.initialize_cycles(repeat_cycles)

            self.number_cycles = repeat_cycles
            self.update_cycle_count_label()
            
            self.update_default_display()
            self.cycles_lbl.config(text="Cycles: {}".format(repeat_cycles))
            volume = self.volume_slider.get()

            # Check if the preset already exists
            self.cursor.execute("SELECT COUNT(*) FROM Presets WHERE ID = ?", (preset_number,))
            exists = self.cursor.fetchone()[0]

            if exists:
                # Update existing preset
                self.cursor.execute("""UPDATE Presets SET
                    TimerDuration = ?, ShortBreakDuration = ?, LongBreakDuration = ?, RepeatCycles = ?, TimerEndSound = ?, ShortBreakSound = ?, LongBreakSound = ?, BackgroundColor = ?, Volume = ?
                    WHERE ID = ?""",
                    (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                    self.timer_end_sound, self.short_break_sound, self.long_break_sound,
                    self.background_color, volume, preset_number))
                print(f"Preset '{preset_number}' settings updated successfully!")
            else:
                # Insert new preset
                self.cursor.execute("""INSERT INTO Presets (
                    ID, TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (preset_number, timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                self.timer_end_sound, self.short_break_sound, self.long_break_sound,
                self.background_color, volume))
                print(f"Preset '{preset_number}' settings saved successfully!")
            
            self.conn.commit()

        def load_preset_settings(preset_number):
            self.cursor.execute(
                "SELECT TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume FROM Presets WHERE ID = ?",
                (preset_number,)
            )
            row = self.cursor.fetchone()
            if row:
                # Unpack the row into variables
                (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                timer_end_sound, short_break_sound, long_break_sound, background_color, volume) = row

                # Update UI with loaded settings
                self.timer_entry.delete(0, END)
                self.timer_entry.insert(0, str(timer_duration // 60))  # minutes
                self.timerseconds_entry.delete(0, END)
                self.timerseconds_entry.insert(0, str(timer_duration % 60))  # seconds

                self.shortbreak_entry.delete(0, END)
                self.shortbreak_entry.insert(0, str(shortbreak_duration // 60))
                self.shortbreakseconds_entry.delete(0, END)
                self.shortbreakseconds_entry.insert(0, str(shortbreak_duration % 60))

                self.longbreak_entry.delete(0, END)
                self.longbreak_entry.insert(0, str(longbreak_duration // 60))
                self.longbreakseconds_entry.delete(0, END)
                self.longbreakseconds_entry.insert(0, str(longbreak_duration % 60))

                self.repeat_cycles_entry.delete(0, END)
                self.repeat_cycles_entry.insert(0, str(repeat_cycles))

                self.alarm_sound_combobox.set(timer_end_sound)
                self.SB_sound_combobox.set(short_break_sound)
                self.LB_sound_combobox.set(long_break_sound)

                self.default_timer_duration = timer_duration
                self.default_remaining_time = timer_duration

                self.default_shortbreak_duration = shortbreak_duration
                self.default_longbreak_duration = longbreak_duration

                self.initialize_cycles(repeat_cycles)

                self.timer_end_sound = timer_end_sound
                self.short_break_sound = short_break_sound
                self.long_break_sound = long_break_sound

                self.background_color = background_color
                self.volume = volume

                # Apply settings to UI
                self.root.configure(bg=background_color)
                self.timer_lbl.configure(bg=background_color)
                self.cycles_lbl.configure(bg=background_color)
                self.session_type_lbl.configure(bg=background_color)
                self.update_cycle_count_label()
                self.update_default_display()
                # Apply volume to volume slider
                self.volume_slider.set(volume)
                print(f"Preset {preset_number} settings loaded successfully!")
            else:
                print(f"No settings found for Preset {preset_number}.")

#Reset All Entry Boxes and Revert to Original Default Mode
        def reset_default_mode():
            self.default_remaining_time = 1500
            self.default_shortbreak_duration = 300
            self.default_longbreak_duration = 900
            self.update_default_display()

            self.default_remaining_time = self.default_timer_duration
            self.timer_type = "default_timer"

            self.number_cycles= 0
            self.current_cycle = 0
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

            root.configure(bg="IndianRed")
            self.timer_lbl.configure(bg="IndianRed")
            self.cycles_lbl.configure(bg="IndianRed")
            self.session_type_lbl.configure(bg="IndianRed")

            self.alarm_sound_combobox.set("Default Alarm")
            self.SB_sound_combobox.set("Default Short Break")
            self.LB_sound_combobox.set("Default Microwave")

            self.timer_end_sound = self.sound_files["Default Alarm"]
            self.short_break_sound = self.sound_files["Default Short Break"]
            self.long_break_sound = self.sound_files["Default Microwave"]
            self.volume = 50
            # Reset volume slider to 50
            self.volume_slider.set(50)
            # Reset all three presets to original defaults
            for preset_number in range(1, 4):
                # Get the original default settings for each preset from the Presets table
                self.cursor.execute(
                    "SELECT TimerDuration, ShortBreakDuration, LongBreakDuration, RepeatCycles, TimerEndSound, ShortBreakSound, LongBreakSound, BackgroundColor, Volume FROM Presets WHERE ID = ?",
                    (preset_number,)
                )
                row = self.cursor.fetchone()
                if row:
                    # Unpack the row into variables
                    (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                    timer_end_sound, short_break_sound, long_break_sound, background_color, volume) = row

                    # Update the preset with the original default values
                    self.cursor.execute("""UPDATE Presets SET
                        TimerDuration = ?, ShortBreakDuration = ?, LongBreakDuration = ?, RepeatCycles = ?, TimerEndSound = ?, ShortBreakSound = ?, LongBreakSound = ?, BackgroundColor = ?, Volume = ?
                        WHERE ID = ?""",
                        (timer_duration, shortbreak_duration, longbreak_duration, repeat_cycles,
                        timer_end_sound, short_break_sound, long_break_sound,
                        "IndianRed", 50, preset_number))  # Hardcode default background color and volume

                    # Commit changes to the database
                    self.conn.commit()

            # Commit changes to the database after resetting all presets
            self.conn.commit()

#Settings Window
        def open_settings():
            settings_window = Toplevel(root)
            settings_window.title("Settings")
            settings_window.geometry("500x500")
            settings_window.configure(bg ="gray")

            settings_window.columnconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform ='a')
            settings_window.rowconfigure((0,1,2,3,4,5,6,7,8,9),weight = 1, uniform='a')
#####################################################################################################################

#Timer Entry
            self.timer_entry_lbl= Label(settings_window, text="Timer Duration (min:sec)", font=("Arial",18), bg="gray", fg="black")
            self.timer_entry_lbl.grid(row = 0, column=1,columnspan=3, sticky="w")

            self.timer_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.timer_entry.grid(row = 0, column=4, columnspan=1, padx=10, pady=5)
            self.timer_entry.insert(0,"25")

            self.timerseconds_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.timerseconds_entry.grid(row = 0, column =5, columnspan =1, padx=10, pady=5)
            self.timerseconds_entry.insert(0,"00")

        #Short Break Entry
            self.shortbreak_entry_lbl= Label(settings_window, text="Short Break Duration (min:sec)", font=("Arial",18), bg="gray", fg="black")
            self.shortbreak_entry_lbl.grid(row = 1, column=1, columnspan=3, sticky="w")

            self.shortbreak_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.shortbreak_entry.grid(row = 1, column=4, columnspan=1, padx=10, pady=5)
            self.shortbreak_entry.insert(0,"5")

            self.shortbreakseconds_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.shortbreakseconds_entry.grid(row = 1, column = 5, columnspan=1, padx=10, pady=5)
            self.shortbreakseconds_entry.insert(0, "00")

        #Long Break Entry
            self.longbreak_entry_lbl= Label(settings_window, text="Long Break Duration (min:sec)", font=("Arial",18), bg="gray", fg="black")
            self.longbreak_entry_lbl.grid(row = 2, column=1, columnspan=3, sticky="w")

            self.longbreak_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.longbreak_entry.grid(row = 2, column=4, columnspan=1, padx=10, pady=5)
            self.longbreak_entry.insert(0,"15")

            self.longbreakseconds_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.longbreakseconds_entry.grid(row = 2, column=5, columnspan=1, padx=10, pady=5)
            self.longbreakseconds_entry.insert(0, "00")

        #Repeat Cycles Entry
            self.repeat_cycles_lbl= Label(settings_window, text="Number of Cycles to Repeat:", font=("Arial",18), bg="gray", fg="black")
            self.repeat_cycles_lbl.grid(row = 3, column=1, columnspan=3, sticky="w")

            self.repeat_cycles_entry = Entry(settings_window, font=("Arial",13), width=7)
            self.repeat_cycles_entry.grid(row = 3, column=4, columnspan=1, padx=10, pady=5)

        #RESET Settings Button
            self.reset_all_btn=Button(settings_window, text="RESET ALL PRESETS", font=("Arial",15), bg="red", fg="black", activebackground="red", command=reset_default_mode)
            self.reset_all_btn.grid(row=9,column=9,columnspan=2,sticky="nsew")
##############################################################################################################

#Sounds Settings
            self.sounds_entry_lbl= Label(settings_window, text="Sounds Options:", font=("Arial",18), bg="gray", fg="black")
            self.sounds_entry_lbl.grid(row = 4, column=1,columnspan=3, sticky="w")

            alarm_options = ["Default Alarm","Referee Whistle","Chime","Default Short Break","Churchbell","Wind Chimes","Default Microwave", "Great Harp", "Relaxing Harp"]
            SB_options = ["Default Short Break", "Churchbell", "Wind Chimes","Default Alarm","Referee Whistle","Chime","Default Microwave", "Great Harp", "Relaxing Harp"]
            LB_options = ["Default Microwave", "Great Harp", "Relaxing Harp","Default Alarm","Referee Whistle","Chime","Default Short Break","Churchbell","Wind Chimes"]

            self.alarm_sound_combobox = ttk.Combobox(settings_window, values=alarm_options, font=("Arial",13))
            self.alarm_sound_combobox.current(0)
            self.alarm_sound_combobox.grid(row=4, column=4, columnspan=2)

            self.SB_sound_combobox = ttk.Combobox(settings_window, values=SB_options, font=("Arial",13))
            self.SB_sound_combobox.current(0)
            self.SB_sound_combobox.grid(row=4, column=6, columnspan=2)

            self.LB_sound_combobox = ttk.Combobox(settings_window, values=LB_options, font=("Arial",13))
            self.LB_sound_combobox.current(0)
            self.LB_sound_combobox.grid(row=4, column=8, columnspan=2)

            self.alarm_sound_combobox.bind("<<ComboboxSelected>>")
            self.SB_sound_combobox.bind("<<ComboboxSelected>>")
            self.LB_sound_combobox.bind("<<ComboboxSelected>>")

            self.selected_alarm_sound = "Default Alarm"
            self.selected_SB_sound = "Default Short Break"
            self.selected_LB_sound = "Default Microwave LB"

            self.bg_color_lbl = Label(settings_window, text="Background Color:", font=("Arial",18), bg="gray", fg="black")
            self.bg_color_lbl.grid(row = 5, column=1,columnspan=3, sticky="w")
            self.bg_color_btn = Button(settings_window, text="Background Color", font=("Arial",13), bg="white", fg="black", command=open_color)
            self.bg_color_btn.grid(row=5, column=4, columnspan =2)

            # Volume Slider
            volume_label = Label(settings_window, text="Sound Volume:", font=("Arial", 18), bg="gray", fg="black")
            volume_label.grid(row=6, column=1, columnspan=3, sticky="w")

            self.volume_slider = Scale(settings_window, from_=0, to=100, orient=HORIZONTAL, command=update_volume, font=("Arial", 13))
            self.volume_slider.set(self.volume)
            self.volume_slider.grid(row=6, column=4, columnspan=3)

            self.volume_label = Label(settings_window, text=f"Volume: {self.volume}%", font=("Arial", 17), bg="gray", fg="black")
            self.volume_label.grid(row=6, column=7, columnspan=2, sticky="w")

            self.preset1_label = Label(settings_window, text="Preset 1:", font=("Arial", 18), bg="gray", fg="black")
            self.preset1_label.grid(row=7, column=1, columnspan=2, sticky="w")

            self.save_preset1_btn=Button(settings_window, text="Save", font=("Arial",10), bg="white", fg="black", command=save_preset1_settings, borderwidth=2, relief="raised")
            self.save_preset1_btn.grid(row=7,column=3,columnspan=1,sticky="nsew")
            self.save_preset1_btn.configure(highlightbackground="blue", highlightcolor="blue", highlightthickness=2)

            self.load_preset1_btn=Button(settings_window, text="Load", font=("Arial",10), bg="white", fg="black", command=load_preset1_settings)
            self.load_preset1_btn.grid(row=7,column=5,columnspan=1,sticky="nsew")

            self.preset2_label = Label(settings_window, text="Preset 2:", font=("Arial", 18), bg="gray", fg="black")
            self.preset2_label.grid(row=8, column=1, columnspan=2, sticky="w")

            self.save_preset2_btn=Button(settings_window, text="Save", font=("Arial",10), bg="white", fg="black", command=save_preset2_settings)
            self.save_preset2_btn.grid(row=8,column=3,columnspan=1,sticky="nsew")

            self.load_preset2_btn=Button(settings_window, text="Load", font=("Arial",10), bg="white", fg="black", command=load_preset2_settings)
            self.load_preset2_btn.grid(row=8,column=5,columnspan=1,sticky="nsew")

            self.preset3_label = Label(settings_window, text="Preset 3:", font=("Arial", 18), bg="gray", fg="black")
            self.preset3_label.grid(row=9, column=1, columnspan=2, sticky="w")

            self.save_preset3_btn=Button(settings_window, text="Save", font=("Arial",10), bg="white", fg="black", command=save_preset3_settings)
            self.save_preset3_btn.grid(row=9,column=3,columnspan=1,sticky="nsew")

            self.load_preset3_btn=Button(settings_window, text="Load", font=("Arial",10), bg="white", fg="black", command=load_preset3_settings)
            self.load_preset3_btn.grid(row=9,column=5,columnspan=1,sticky="nsew")

#MENU Taskbar
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
        self.defaultcurrent_SB_lbl = Label(root, text="Lets take a Short Break!", font=("Times", 16), fg="black", bg="IndianRed")
        self.defaultcurrent_LB_lbl = Label(root, text="Lets take a Long Break!", font=("Times", 16), fg="black", bg="IndianRed")

        self.default_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_default_time)
        self.default_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_default_time)
        self.default_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_default_time)

    #Study Mode Buttons and Label
        self.study_timer_lbl = Label(root, text = "45:00", font= ("Times", 100,), fg ="black", bg = "cornflowerblue")
        self.studycurrent_SB_lbl = Label(root, text="Lets take a Short Break!", font=("Times", 16), fg="black", bg="cornflowerblue")
        self.studycurrent_LB_lbl = Label(root, text="Lets take a Long Break!", font=("Times", 16), fg="black", bg="cornflowerblue")

        self.study_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_study_time)
        self.study_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_study_time)
        self.study_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_study_time)
    
    #Relax Mode Label and Buttons
        self.relax_timer_lbl = Label(root, text = "15:00", font= ("Times", 100,), fg ="black", bg = "mediumseagreen")
        self.relaxcurrent_SB_lbl = Label(root, text="Lets take a Short Break!", font=("Times", 16), fg="black", bg="mediumseagreen")
        self.relaxcurrent_LB_lbl = Label(root, text="Lets take a Long Break!", font=("Times", 16), fg="black", bg="mediumseagreen")

        self.relax_start_btn = Button(text = "Start", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.start_relax_time)
        self.relax_stop_btn = Button(text = "Stop", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.pause_relax_time)
        self.relax_reset_btn = Button(text = "Reset", font= ("Times", 16), fg = "black", activebackground = "grey",command =self.reset_relax_time)

        self.session_type_lbl = Label(root, text="", font=("Times", 16), fg="black", bg="IndianRed")
        self.study_session_type_lbl = Label(root, text="", font=("Times", 16), fg="black", bg="cornflowerblue") 
        self.relax_session_type_lbl = Label(root, text="", font=("Times", 16), fg="black", bg="mediumseagreen") 

        switch_default_mode()

###########################################################################################################
#DEFAULT#
# Default mode timer variables
        self.default_run_timer = False
        self.default_start_timer = 0
        self.default_pause_timer = False
        self.default_timer_duration = 1500
        self.default_remaining_time = self.default_timer_duration
        self.default_shortbreak_duration = 300  # Default short break duration in seconds
        self.default_longbreak_duration = 900   # Default long break duration in seconds

        self.timer_type = "default_timer"

        self.default_timer_sound = "Default Timer Alarm.wav"
        self.default_short_break_sound = "Default SB.wav"
        self.default_long_break_sound = "Default Microwave LB.wav"

        self.number_cycles = 0  # Initialize number of cycles to zero
        self.current_cycle = 0  #Current cycles is zero
        self.update_cycle_count_label()

    def complete_pomodoro_session(self, mode, timer_duration, short_break_duration, long_break_duration):
        self.insert_pomodoro_session(mode, 'Timer', timer_duration)
        if short_break_duration is not None:
            self.insert_pomodoro_session(mode, 'Short Break', short_break_duration)
        if long_break_duration is not None:
            self.insert_pomodoro_session(mode, 'Long Break', long_break_duration)

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
            cycle_sequence_length = 9  # Length of the cycle sequence
            current_cycle_in_sequence = self.current_cycle % cycle_sequence_length
            
            # Determine the phase of the current cycle based on the sequence
            if current_cycle_in_sequence % 9 != 8:  # Timer or Short Break phase
                if current_cycle_in_sequence % 2 == 0:  # Timer phase
                    self.timer_type = "default_timer"
                    self.default_remaining_time = self.default_timer_duration
                    self.start_default_time()  # Start the timer
                else:  # Short break phase
                    self.timer_type = "short_break"
                    self.default_remaining_time = self.default_shortbreak_duration
                    self.start_default_time()  # Start the short break
            else:  # Long break phase
                self.timer_type = "long_break"
                self.default_remaining_time = self.default_longbreak_duration
                self.start_default_time()  # Start the long break
                # Reset current cycle to 0 after Long Break
                self.current_cycle = 0
                # Update cycle count label
                self.number_cycles -= 1
                self.update_cycle_count_label()
                return  # Skip the rest of the method after the long break

        else:
            # Handle case when no cycles left
            self.number_cycles = 0
            self.update_cycle_count_label()  # Update cycle count label

        self.current_cycle += 1

    def update_default_time(self):
        if self.default_run_timer:
            current_time = time.time()  # Get current time and find the time passed since it started
            time_passed = current_time - self.default_start_timer
            self.default_remaining_time = max(self.default_remaining_time - time_passed, 0)  # Prevents remaining time from becoming less than 0
            self.update_default_display()

            if self.default_remaining_time > 0:
                self.default_start_timer = current_time
                self.root.after(1000, self.update_default_time)
            else:
                # Timer has ended
                self.default_run_timer = False
                self.alarm_sound(self.timer_type)

                if self.timer_type == "default_timer":
                    self.complete_pomodoro_session("Default", self.default_timer_duration, None, "Timer")
                elif self.timer_type == "short_break":
                    self.complete_pomodoro_session("Default", self.default_shortbreak_duration, None, "Short Break")
                elif self.timer_type == "long_break":
                    self.complete_pomodoro_session("Default", self.default_longbreak_duration, None, "Long Break")

                # Wait for the sound to finish before starting the next session
                sound_length = pygame.mixer.Sound(self.timer_end_sound).get_length() * 1000  # Convert seconds to milliseconds
                self.root.after(int(sound_length), self.start_cycle) 
                self.update_default_display()
                # Update cycle count label
                self.update_cycle_count_label()

    # Call this method to start the pomodoro cycles
    def initialize_cycles(self, number_of_cycles):
        self.number_cycles = number_of_cycles  # Initialize number of cycles
        self.current_cycle = 0
        self.start_cycle()

    def update_default_display(self):
        minutes = int(self.default_remaining_time // 60)
        seconds = int(self.default_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)
        self.update_session_type_label()

    def update_cycle_count_label(self):
        # Ensure cycle count doesn't go below zero
        self.number_cycles = max(self.number_cycles, 0)
        self.cycles_lbl.config(text="Cycles: {}".format(self.number_cycles))

    def update_session_type_label(self):
        # Update session type label based on the current session type
        if self.timer_type == "default_timer":
            session_type = "Timer"
        elif self.timer_type == "short_break":
            session_type = "Short Break"
        elif self.timer_type == "long_break":
            session_type = "Long Break"
        else:
            session_type = ""
        
        self.session_type_lbl.config(text=session_type)

    def alarm_sound(self, timer_type):
        if timer_type == "default_timer":
            self.play_sound(self.timer_end_sound)
        elif timer_type == "short_break":
            self.play_sound(self.short_break_sound)
        elif timer_type == "long_break":
            self.play_sound(self.long_break_sound)

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

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
        self.study_cycle_count = 0

        #Load sounds
        self.study_timer_sound = pygame.mixer.Sound("Study Referee Alarm.wav")
        self.study_shortbreak_sound = pygame.mixer.Sound("Study Churchbell SB.wav")
        self.study_longbreak_sound = pygame.mixer.Sound("Study Great Harp LB.wav")


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
            self.study_remaining_time = self.study_longbreak_duration
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
                self.alarm_sound2(self.study_type)

                if self.study_type == "study_timer":
                    self.study_type = "study_shortbreak"
                    self.study_remaining_time = self.study_shortbreak_duration
                    self.complete_pomodoro_session("Study", self.study_shortbreak_duration, None, "Short Break")
                    self.start_study_time()  # Start short break timer automatically
                elif self.study_type == "study_shortbreak":
                    self.study_cycle_count += 1
                    if self.study_cycle_count < 4:
                        self.study_type = "study_timer"
                        self.study_remaining_time = self.study_timer_duration
                        self.complete_pomodoro_session("Study", self.study_timer_duration, None, "Timer")
                        self.start_study_time()  # Start timer automatically
                    else:
                        self.study_type = "study_longbreak"
                        self.study_remaining_time = self.study_longbreak_duration
                        self.complete_pomodoro_session("Study", self.study_longbreak_duration, None, "Long Break")
                        self.study_cycle_count = 0  # Reset cycle count after long break
                        self.start_study_time()  # Start long break timer automatically
                        # Calculate the length of the sound file in milliseconds
                # Update the display with the new timer type and remaining time
                self.update_study_display()


    def update_study_display(self):
        minutes = int(self.study_remaining_time // 60)
        seconds = int(self.study_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.study_timer_lbl.config(text=time_str)
        self.update_study_session_type_label()

    def update_study_session_type_label(self):
        # Update session type label based on the current session type
        if self.study_type == "study_timer":
            study_session_type = "Timer"
        elif self.study_type == "study_shortbreak":
            study_session_type = "Short Break"
        elif self.study_type == "study_longbreak":
            study_session_type = "Long Break"
        else:
            study_session_type = ""
        
        self.study_session_type_lbl.config(text=study_session_type)

    def alarm_sound2(self,study_type):
        # Stop any currently playing sound
        pygame.mixer.stop()

        if study_type == "study_timer":
            self.study_timer_sound.play()
        elif study_type == "study_shortbreak":
            self.study_shortbreak_sound.play()
        elif study_type == "study_longbreak":
            self.study_longbreak_sound.play()

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
        self.relax_cycle_count = 0

        #Load sounds
        self.relax_timer_sound = pygame.mixer.Sound("Relax Chime Alarm.wav")
        self.relax_shortbreak_sound = pygame.mixer.Sound("Relax WindChimes SB.wav")
        self.relax_longbreak_sound = pygame.mixer.Sound("Relax Harp LB.wav")

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
                self.alarm_sound3(self.relax_type)

                if self.relax_type == "relax_timer":
                    self.relax_type = "relax_shortbreak"
                    self.relax_remaining_time = self.relax_shortbreak_duration
                    self.complete_pomodoro_session("Relax", self.relax_shortbreak_duration, None, "Short Break")
                    self.start_relax_time()  # Start short break timer automatically
                elif self.relax_type == "relax_shortbreak":
                    self.relax_cycle_count += 1
                    if self.relax_cycle_count < 4:
                        self.relax_type = "relax_timer"
                        self.relax_remaining_time = self.relax_timer_duration
                        self.complete_pomodoro_session("Relax", self.study_timer_duration, None, "Timer")
                        self.start_relax_time()  # Start timer automatically
                    else:
                        self.relax_type = "relax_longbreak"
                        self.relax_remaining_time = self.relax_longbreak_duration
                        self.complete_pomodoro_session("Relax", self.study_longbreak_duration, None, "Long Break")
                        self.relax_cycle_count = 0  # Reset cycle count after long break
                        self.start_relax_time()  # Start long break timer automatically

                # Update the display with the new timer type and remaining time
                self.update_relax_display()


    def update_relax_display(self):
        minutes = int(self.relax_remaining_time // 60)
        seconds = int(self.relax_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.relax_timer_lbl.config(text=time_str)
        self.update_relax_session_type_label()

    def update_relax_session_type_label(self):
        # Update session type label based on the current session type
        if self.relax_type == "relax_timer":
            relax_session_type = "Timer"
        elif self.relax_type == "relax_shortbreak":
            relax_session_type = "Short Break"
        elif self.relax_type == "relax_longbreak":
            relax_session_type = "Long Break"
        else:
            relax_session_type = ""
        
        self.relax_session_type_lbl.config(text=relax_session_type)

    def alarm_sound3(self,relax_type):
        # Stop any currently playing sound
        pygame.mixer.stop()

        if relax_type == "relax_timer":
            self.relax_timer_sound.play()
        elif relax_type == "relax_shortbreak":
            self.relax_shortbreak_sound.play()
        elif relax_type == "relax_longbreak":
            self.relax_longbreak_sound.play()

    def insert_pomodoro_session(self, mode, session_type, duration, user='John'):
        completion_time = datetime.now().isoformat()  # Get the current completion time

        # Execute the SQL query to insert the session into the table
        self.cursor.execute('''
        INSERT INTO PomodoroSessions (User, Mode, SessionType, Duration, CompletionTime)
        VALUES (?, ?, ?, ?, ?)
        ''', (user, mode, session_type, duration, completion_time))

if __name__ == "__main__":
    root = Tk()
    app = MainInterface(root)
    root.mainloop()
    pygame.quit()