import tkinter as tk
from tkinter import messagebox
import time
import math
import winsound
from PIL import Image, ImageTk

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg="IndianRed")
        
        self.timer_duration = 5  # Timer duration in seconds
        self.remaining_time = self.timer_duration
        self.run_timer = False
        self.start_timer = 0
        self.completed_sessions = 0  # Counter for completed sessions
        self.achievement_threshold1 = 2  # Number of sessions to achieve badge 1
        self.achievement_threshold2 = 3  # Number of sessions to achieve badge 2
        self.sessions_with_5_sec = 0  # Counter for sessions with 5-second duration
        self.sessions_with_10_sec = 0  # Counter for sessions with 10-second duration

        self.create_widgets()

    def create_widgets(self):
        self.timer_lbl = tk.Label(self.root, text="00:05", font=("Times", 180), fg="black", bg="IndianRed")
        self.timer_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.start_btn = tk.Button(self.root, text="Start", font=("Times", 16), fg="black", activebackground="grey", command=self.start_time, width=10, height=1)
        self.start_btn.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.stop_btn = tk.Button(self.root, text="Stop", font=("Times", 16), fg="black", activebackground="grey", command=self.pause_time, state=tk.DISABLED, width=10, height=1)
        self.stop_btn.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

        self.reset_btn = tk.Button(self.root, text="Reset", font=("Times", 16), fg="black", activebackground="grey", command=self.reset_time, width=10, height=1)
        self.reset_btn.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

    def start_time(self):
        if not self.run_timer:
            self.run_timer = True
            self.start_timer = time.time()
            self.update_time()
            self.start_btn.configure(state=tk.DISABLED)
            self.stop_btn.configure(state=tk.NORMAL)

    def pause_time(self):
        if self.run_timer:
            self.run_timer = False
            self.start_btn.configure(state=tk.NORMAL)
            self.stop_btn.configure(state=tk.DISABLED)

    def reset_time(self):
        self.run_timer = False
        if self.completed_sessions >= self.achievement_threshold1:
            self.timer_duration = 10  # Set timer duration to 10 seconds if badge 1 achieved
        self.remaining_time = self.timer_duration
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.update_display()

    def update_time(self):
        if self.run_timer:
            current_time = time.time()
            time_passed = current_time - self.start_timer
            self.remaining_time = max(self.remaining_time - time_passed, 0)
            self.update_display()

            if self.remaining_time > 0:
                self.start_timer = current_time
                self.root.after(1000, self.update_time)
            else:
                self.run_timer = False
                self.completed_sessions += 1  # Increment completed sessions
                if self.timer_duration == 5:
                    self.sessions_with_5_sec += 1
                    if self.sessions_with_5_sec >= self.achievement_threshold1:
                        self.achievement_unlocked(1)
                elif self.timer_duration == 10:
                    self.sessions_with_10_sec += 1
                    if self.sessions_with_10_sec >= self.achievement_threshold2:
                        self.achievement_unlocked(2)

    def update_display(self):
        # Round up the remaining time to the nearest second
        seconds = math.ceil(self.remaining_time)
        minutes = seconds // 60
        seconds %= 60
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

    def achievement_unlocked(self, badge_num):
        winsound.Beep(440, 500)  # Beep sound to indicate achievement
        if badge_num == 1:
            messagebox.showinfo("Achievement Unlocked!", "You've completed 2 sessions with 5 seconds!")
            self.sessions_with_5_sec = 0
            self.display_badge(badge_num, "badge1.png")
        elif badge_num == 2:
            messagebox.showinfo("Achievement Unlocked!", "You've completed 3 sessions with 10 seconds!")
            self.sessions_with_10_sec = 0
            self.display_badge(badge_num, "badge2.png")

    def display_badge(self, badge_num, badge_path):
        badge_window = tk.Toplevel(self.root)
        badge_window.title("Badge " + str(badge_num))
        
        # Open the image with Pillow
        badge_image_pil = Image.open("badge1.png")
        
        # Convert the image to a format usable by Tkinter
        badge_image_tk = ImageTk.PhotoImage(badge_image_pil)
        
        # Create a label to display the image
        badge_label = tk.Label(badge_window, image=badge_image_tk)
        badge_label.image = badge_image_tk  # Keep reference to the image to prevent garbage collection
        badge_label.pack()

root = tk.Tk()
pomodoro_timer = PomodoroTimer(root)
root.mainloop()
