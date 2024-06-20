import tkinter as tk
from tkinter import messagebox
import time
import math
import winsound
from PIL import Image, ImageTk

# Constants
BG_COLOR = "IndianRed"
FONT_STYLE = ("Times", 16)
TIMER_FONT_STYLE = ("Times", 180)
BEEP_FREQUENCY = 440
BEEP_DURATION = 500

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg=BG_COLOR)

        self.timer_duration = 5  # Initial duration set to 5 seconds
        self.remaining_time = self.timer_duration
        self.run_timer = False
        self.start_timer = 0
        self.cumulative_time = 0  # Cumulative time counter
        self.badges = {5: "badge1.png", 15: "badge2.png", 40: "badge3.png"}  # Dictionary of badges and their cumulative time thresholds
        self.collected_badges = []  # List to store collected badges

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Timer Label
        self.timer_lbl = tk.Label(main_frame, text="00:05", font=TIMER_FONT_STYLE, fg="black", bg=BG_COLOR)
        self.timer_lbl.pack(pady=50)

        # Button Frame
        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(btn_frame, text="Start", font=FONT_STYLE, fg="black", activebackground="grey", command=self.start_time, width=10, height=1)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop", font=FONT_STYLE, fg="black", activebackground="grey", command=self.pause_time, state=tk.DISABLED, width=10, height=1)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = tk.Button(btn_frame, text="Reset", font=FONT_STYLE, fg="black", activebackground="grey", command=self.reset_time, width=10, height=1)
        self.reset_btn.grid(row=0, column=2, padx=10)

        self.view_badges_btn = tk.Button(main_frame, text="View Badges", font=FONT_STYLE, fg="black", activebackground="grey", command=self.view_collected_badges, width=15, height=1)
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
                time_used = self.timer_duration - self.remaining_time
                self.cumulative_time += time_used
                self.check_achievements()

    def update_display(self):
        # Round up the remaining time to the nearest second
        seconds = math.ceil(self.remaining_time)
        minutes = seconds // 60
        seconds %= 60
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_lbl.config(text=time_str)

    def check_achievements(self):
        for threshold, badge_path in self.badges.items():
            if self.cumulative_time >= threshold and badge_path not in self.collected_badges:
                self.collected_badges.append(badge_path)
                self.achievement_unlocked(badge_path)

    def achievement_unlocked(self, badge_path):
        winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)
        messagebox.showinfo("Achievement Unlocked!", "You've earned a new badge!")
        self.display_badge(badge_path)

    def display_badge(self, badge_path):
        badge_window = tk.Toplevel(self.root)
        badge_window.title(f"Badge {badge_path}")
        
        badge_image_pil = Image.open(badge_path)
        badge_image_tk = ImageTk.PhotoImage(badge_image_pil)
        
        badge_label = tk.Label(badge_window, image=badge_image_tk)
        badge_label.image = badge_image_tk
        badge_label.pack()

    def display_badge(self, badge_path):
        badge_name = os.path.basename(badge_path)
        badge_window = tk.Toplevel(self.root)
        badge_window.title(f"Badge {badge_name}")

        # Load badge image using os module
        badge_image = tk.PhotoImage(file=badge_path)
        
        badge_label = Label(badge_window, image=badge_image)
        badge_label.image = badge_image
        badge_label.pack()

    def view_collected_badges(self):
        badges_window = tk.Toplevel(self.root)
        badges_window.title("Collected Badges")
        badges_window.geometry("400x300")
        
        for i, badge_path in enumerate(self.collected_badges):
            badge_image_pil = Image.open(badge_path)
            badge_image_tk = ImageTk.PhotoImage(badge_image_pil)
            
            badge_label = tk.Label(badges_window, image=badge_image_tk)
            badge_label.image = badge_image_tk
            badge_label.grid(row=i // 2, column=i % 2, padx=10, pady=10)


class MainInterface(PomodoroTimer):
    def __init__(self, root):
        super().__init__(root)
        # Your existing code here
        # Merge the additional functionalities from your existing codebase with the PomodoroTimer class


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()