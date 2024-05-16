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

        self.timer_duration = 2  # Initial duration set to 2 seconds
        self.remaining_time = self.timer_duration
        self.run_timer = False
        self.start_timer = 0
        self.completed_sessions = 0  # Counter for completed sessions
        self.achievement_threshold1 = 2  # Number of sessions to achieve badge 1
        self.achievement_threshold2 = 3  # Number of sessions to achieve badge 2
        self.achievement_threshold3 = 4  # Number of sessions to achieve badge 3
        self.achievement_threshold4 = 5  # Number of sessions to achieve badge 4
        self.sessions_with_2_sec = 0  # Counter for sessions with 2-second duration
        self.sessions_with_3_sec = 0  # Counter for sessions with 3-second duration
        self.sessions_with_4_sec = 0  # Counter for sessions with 4-second duration
        self.sessions_with_5_sec = 0  # Counter for sessions with 5-second duration
        self.collected_badges = []  # List to store collected badges

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg="IndianRed")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Timer Label
        self.timer_lbl = tk.Label(main_frame, text="00:02", font=("Times", 180), fg="black", bg="IndianRed")
        self.timer_lbl.pack(pady=50)

        # Button Frame
        btn_frame = tk.Frame(main_frame, bg="IndianRed")
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(btn_frame, text="Start", font=("Times", 16), fg="black", activebackground="grey", command=self.start_time, width=10, height=1)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop", font=("Times", 16), fg="black", activebackground="grey", command=self.pause_time, state=tk.DISABLED, width=10, height=1)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = tk.Button(btn_frame, text="Reset", font=("Times", 16), fg="black", activebackground="grey", command=self.reset_time, width=10, height=1)
        self.reset_btn.grid(row=0, column=2, padx=10)

        self.view_badges_btn = tk.Button(main_frame, text="View Badges", font=("Times", 16), fg="black", activebackground="grey", command=self.view_collected_badges, width=15, height=1)
        self.view_badges_btn.pack(pady=20)

    def start_time(self):
        if not self.run_timer:
            self.run_timer = True
            self.start_timer = time.perf_counter()
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
        self.update_timer_duration()  # Update timer duration based on achievements
        self.remaining_time = self.timer_duration
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.update_display()

    def update_time(self):
        if self.run_timer:
            current_time = time.perf_counter()
            time_passed = current_time - self.start_timer
            self.remaining_time = max(self.remaining_time - time_passed, 0)
            self.update_display()

            if self.remaining_time > 0:
                self.start_timer = current_time
                self.root.after(100, self.update_time)
            else:
                self.run_timer = False
                self.completed_sessions += 1  # Increment completed sessions
                self.check_achievements()

    def update_display(self):
        # Round up the remaining time to the nearest second
        seconds = math.ceil(self.remaining_time)
        minutes = seconds // 60
        seconds %= 60
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

    def update_timer_duration(self):
        # Check the current thresholds and update the timer duration
        if self.sessions_with_2_sec >= self.achievement_threshold1:
            self.timer_duration = 3  # Upgrade timer duration to 3 seconds if badge 1 achieved
            self.sessions_with_2_sec = 0  # Reset the 2-second sessions counter
        if self.sessions_with_3_sec >= self.achievement_threshold2:
            self.timer_duration = 4  # Upgrade timer duration to 4 seconds if badge 2 achieved
            self.sessions_with_3_sec = 0  # Reset the 3-second sessions counter
        if self.sessions_with_4_sec >= self.achievement_threshold3:
            self.timer_duration = 5  # Upgrade timer duration to 5 seconds if badge 3 achieved
            self.sessions_with_4_sec = 0  # Reset the 4-second sessions counter
        if self.sessions_with_5_sec >= self.achievement_threshold4:
            self.timer_duration = 15  # Upgrade timer duration to 15 seconds if badge 4 achieved
            self.sessions_with_5_sec = 0  # Reset the 5-second sessions counter

    def check_achievements(self):
        if self.timer_duration == 2:
            self.sessions_with_2_sec += 1
            if self.sessions_with_2_sec >= self.achievement_threshold1:
                self.achievement_unlocked(1)
        elif self.timer_duration == 3:
            self.sessions_with_3_sec += 1
            if self.sessions_with_3_sec >= self.achievement_threshold2:
                self.achievement_unlocked(2)
        elif self.timer_duration == 4:
            self.sessions_with_4_sec += 1
            if self.sessions_with_4_sec >= self.achievement_threshold3:
                self.achievement_unlocked(3)
        elif self.timer_duration == 5:
            self.sessions_with_5_sec += 1
            if self.sessions_with_5_sec >= self.achievement_threshold4:
                self.achievement_unlocked(4)

    def achievement_unlocked(self, badge_num):
        winsound.Beep(440, 500)  # Beep sound to indicate achievement
        if badge_num == 1:
            messagebox.showinfo("Achievement Unlocked!", "You've completed 2 sessions with 2 seconds!")
            self.display_badge(badge_num, "badge1.png")
        elif badge_num == 2:
            messagebox.showinfo("Achievement Unlocked!", "You've completed 3 sessions with 3 seconds!")
            self.display_badge(badge_num, "badge4.png")
        elif badge_num == 3:
            messagebox.showinfo("Achievement Unlocked!", "You've completed 4 sessions with 4 seconds!")
            self.display_badge(badge_num, "badge3.png")
        elif badge_num == 4:
            messagebox.showinfo("Achivement Unlocked!", "You've completed 5 sessions with 5 seconds!")
            self.display_badge(badge_num, "badge2.png")

    def display_badge(self, badge_num, badge_path):
        self.collected_badges.append(badge_path)  # Add badge path to collected badges list
        badge_window = tk.Toplevel(self.root)
        badge_window.title("Badge " + str(badge_num))
        
        # Open the image with Pillow
        badge_image_pil = Image.open(badge_path)
        
        # Convert the image to a format usable by Tkinter
        badge_image_tk = ImageTk.PhotoImage(badge_image_pil)
        
        # Create a label to display the image
        badge_label = tk.Label(badge_window, image=badge_image_tk)
        badge_label.image = badge_image_tk  # Keep reference to the image to prevent garbage collection
        badge_label.pack()

    def view_collected_badges(self):
        badges_window = tk.Toplevel(self.root)
        badges_window.title("Collected Badges")
        badges_window.geometry("400x300")
        
        for i, badge_path in enumerate(self.collected_badges):
            # Open the image with Pillow
            badge_image_pil = Image.open(badge_path)
            
            # Convert the image to a format usable by Tkinter
            badge_image_tk = ImageTk.PhotoImage(badge_image_pil)
            
            # Create a label to display the image
            badge_label = tk.Label(badges_window, image=badge_image_tk)
            badge_label.image = badge_image_tk  # Keep reference to the image to prevent garbage collection
            badge_label.grid(row=i // 2, column=i % 2, padx=10, pady=10)

root = tk.Tk()
pomodoro_timer = PomodoroTimer(root)
root.mainloop()
