import os
import time
import pygame
import sqlite3
from tkinter import *
from tkinter import messagebox

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("1000x700")
        self.root.configure(bg="IndianRed")

        self.window_icon = PhotoImage(file="pomodoro helper.png")
        self.root.iconphoto(False, self.window_icon)

        pygame.init()
        pygame.mixer.init()
        global counter
        counter = 1

        # Defining Grid
        self.root.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')
        self.root.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')

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
        self.background_color = "IndianRed"

        self.badges = {
            5: "badge1.png",
            15: "badge2.png",
            30: "badge3.png"
        }  # Dictionary of badges and their cumulative time thresholds
        self.collected_badges = []  # List to store collected badges
        self.cumulative_time = 0  # Cumulative time counter

        # Check if all badge images exist
        for threshold, badge_path in self.badges.items():
            if not os.path.exists(badge_path):
                print(f"Warning: Badge image {badge_path} does not exist.")

        # Study Mode variables
        self.study_run_timer = False
        self.study_start_timer = 0
        self.study_pause_timer = False
        self.study_timer_duration = 2700
        self.study_remaining_time = self.study_timer_duration
        self.study_shortbreak_duration = 900
        self.study_longbreak_duration = 1500
        self.is_music_playing = False
        self.volume = 50
        self.study_type = "study_timer"
        self.study_cycle_count = 0

        # Relax Mode variables
        self.relax_run_timer = False
        self.relax_start_timer = 0
        self.relax_pause_timer = False
        self.relax_timer_duration = 900
        self.relax_remaining_time = self.relax_timer_duration
        self.relax_shortbreak_duration = 1200
        self.relax_longbreak_duration = 1800

        self.relax_type = "relax_timer"
        self.relax_cycle_count = 0

        self.current_plot = None

        # UI setup
        self.timer_lbl = Label(self.root, text="00:00")
        self.timer_lbl.pack()

        self.session_type_lbl = Label(self.root, text="Session Type")
        self.session_type_lbl.pack()

        self.cycles_lbl = Label(self.root, text=": 0", font=("Times", 20))
        self.cycles_lbl.pack()

    def defaultmode_timer(self):
        self.default_remaining_time = 1500
        self.timer_type = "default_timer"
        self.start_default_time()

    def defaultmode_shortbreak(self):
        self.default_timer_duration = 300
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "short_break"
        self.start_default_time()

    def defaultmode_longbreak(self):
        self.default_timer_duration = 900
        self.default_remaining_time = self.default_timer_duration
        self.timer_type = "long_break"
        self.start_default_time()

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
            self.default_remaining_time = 1500
        elif self.timer_type == "short_break":
            self.default_remaining_time = 300
        else:
            self.default_remaining_time = 900
        self.update_default_display()

    def start_cycle(self):
        if self.number_cycles > 0:
            cycle_sequence_length = 9  # Length of the cycle sequence
            current_cycle_in_sequence = self.current_cycle % cycle_sequence_length

            if current_cycle_in_sequence % 9 != 8:  # Timer or Short Break phase
                if current_cycle_in_sequence % 2 == 0:  # Timer phase
                    self.timer_type = "default_timer"
                    self.default_remaining_time = 1500
                    self.start_default_time()  # Start the timer
                else:  # Short break phase
                    self.timer_type = "short_break"
                    self.default_remaining_time = 300
                    self.start_default_time()  # Start the short break
            else:  # Long break phase
                self.timer_type = "long_break"
                self.default_remaining_time = 900
                self.start_default_time()  # Start the long break
                # Reset current cycle to 0 after Long Break
                self.current_cycle = 0
                # Update cycle count label
                self.number_cycles -= 1
                self.update_cycle_count_label()
                return  # Skip the rest of the method after the long break

        else:
            self.number_cycles = 0
            self.update_cycle_count_label()  # Update cycle count label

        self.current_cycle += 1

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
                self.alarm_sound(self.timer_type)
                self.cumulative_time += time_passed
                self.check_achievements()

                if self.timer_type == "default_timer":
                    self.complete_pomodoro_session("Default", 1500, None, "Timer")
                elif self.timer_type == "short_break":
                    self.complete_pomodoro_session("Default", 300, None, "Short Break")
                elif self.timer_type == "long_break":
                    self.complete_pomodoro_session("Default", 900, None, "Long Break")

                sound_length = pygame.mixer.Sound(self.timer_end_sound).get_length() * 1000
                self.root.after(int(sound_length), self.start_cycle)
                self.update_default_display()
                self.update_cycle_count_label()

    def initialize_cycles(self, number_of_cycles):
        self.number_cycles = number_of_cycles
        self.current_cycle = 0
        self.start_cycle()

    def update_default_display(self):
        minutes = int(self.default_remaining_time // 60)
        seconds = int(self.default_remaining_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)
        self.session_type_lbl.config(text=self.timer_type)

    def update_cycle_count_label(self):
        self.cycles_lbl.config(text=f"Cycles: {self.number_cycles}")

    def alarm_sound(self, timer_type):
        if timer_type == "default_timer":
            pygame.mixer.Sound(self.timer_end_sound).play()
        elif timer_type == "short_break":
            pygame.mixer.Sound(self.short_break_sound).play()
        elif timer_type == "long_break":
            pygame.mixer.Sound(self.long_break_sound).play()

    def check_achievements(self):
        for threshold, badge_path in self.badges.items():
            if self.cumulative_time >= threshold and badge_path not in self.collected_badges:
                self.collected_badges.append(badge_path)
                self.show_badge(badge_path)

    def show_badge(self, badge_path):
        badge_img = PhotoImage(file=badge_path)
        badge_lbl = Label(self.root, image=badge_img)
        badge_lbl.image = badge_img
        badge_lbl.pack()
        self.root.after(5000, badge_lbl.destroy)

    def complete_pomodoro_session(self, user, duration, mode, session_type):
        completion_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""INSERT INTO PomodoroSessions (User, Mode, SessionType, Duration, CompletionTime) 
                               VALUES (?, ?, ?, ?, ?)""",
                            (user, mode, session_type, duration, completion_time))
        self.conn.commit()

root = Tk()
app = MainInterface(root)
root.mainloop()
