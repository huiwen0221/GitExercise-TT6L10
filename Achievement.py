import tkinter as tk
from tkinter import ttk
import calendar

<<<<<<< HEAD
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
=======
class PunchInPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Punch-In Page")
        self.configure(background="light yellow")  # Set background color
        
        self.days_in_month = {
            1: 31,  # January
            2: 28,  # February
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31,  # October
            11: 30,  # November
            12: 31   # December
        }

        # Title frame
        title_frame = tk.Frame(self, background="light yellow")
        title_frame.pack()
>>>>>>> e10262d81f669a1b328b8d701cd09dc2fc306f00

        # Add title label
        self.title_label = tk.Label(title_frame, text="My Achievement", font=("Cooper Black", 50, "bold"), background="light yellow")
        self.title_label.pack(pady=(10, 0))

<<<<<<< HEAD
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
=======
        # Add "Days Matter" label
        self.days_matter = tk.StringVar()
        self.days_matter.set("Days Matter: 0")
        self.days_matter_label = tk.Label(title_frame, textvariable=self.days_matter, font=("Times New Roman", 20), background="light yellow")
        self.days_matter_label.pack(pady=(5, 10))

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set, background="light yellow")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.calendar_frame = tk.Frame(self.canvas, background="light yellow")  # Set background color of the frame
        self.canvas.create_window((0, 0), window=self.calendar_frame, anchor="nw")

        # Create a grid of punch boxes for each day of the year
        self.punch_boxes = []
        self.punch_status = {}  # Dictionary to store the punch status of each day
        self.consecutive_days = 0  # Tracks consecutive punched days
        self.badge_label = None
        self.badge2_label = None
        self.badge3_label = None

        for month in range(1, 13):
            month_name = calendar.month_name[month]
            month_label = tk.Label(self.calendar_frame, text=month_name, font=("Helvetica", 12, "bold"), background="light yellow")
            month_label.grid(row=(month-1)*2, column=1, columnspan=self.days_in_month[month], pady=(10, 0))

            for day in range(1, self.days_in_month[month] + 1):
                punch_box = tk.Label(self.calendar_frame, width=4, height=3, relief="ridge", bg="white")
                punch_box.grid(row=(month-1)*2+1, column=day-1, padx=2, pady=2)
                punch_box.bind("<Button-1>", lambda event, day=day, month=month, punch_box=punch_box: self.punch_in(day, month, punch_box))
                self.punch_boxes.append((day, month, punch_box))
                self.punch_status[(day, month)] = False  # Initialize punch status to False (not punched)

        self.calendar_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Load badge images
        self.badge_image = tk.PhotoImage(file="badge1.png")
        self.badge2_image = tk.PhotoImage(file="badge2.png")
        self.badge3_image = tk.PhotoImage(file="badge3.png")

    def punch_in(self, day, month, punch_box):
        punched_date = (day, month)
        if not self.punch_status[punched_date]:
            if not self.punch_status[punched_date]:
                self.consecutive_days += 1
            else:
                self.consecutive_days = 0
>>>>>>> e10262d81f669a1b328b8d701cd09dc2fc306f00

            self.punch_status[punched_date] = True  # Mark as punched
            punch_box.config(bg="bisque3")  # Change background color to indicate punched

<<<<<<< HEAD
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
=======
        self.update_days_matter()  # Update the "Days Matter" label

    def update_days_matter(self):
        punched_days = sum(1 for status in self.punch_status.values() if status)
        self.days_matter.set(f"Days Matter: {punched_days}")

        if self.consecutive_days in [7, 21, 31]:
            self.show_badge(self.consecutive_days)
        else:
            self.hide_badge()

    def show_badge(self, badge_day):
        if badge_day == 7:
            if not self.badge_label:
                self.badge_label = tk.Label(self, image=self.badge_image, background="light yellow")
                self.badge_label.pack()
        elif badge_day == 21:
            if not self.badge2_label:
                self.badge2_label = tk.Label(self, image=self.badge2_image, background="light yellow")
                self.badge2_label.pack()
        elif badge_day == 31:
            if not self.badge3_label:
                self.badge3_label = tk.Label(self, image=self.badge3_image, background="light yellow")
                self.badge3_label.pack()

    def hide_badge(self):
        if self.badge_label:
            self.badge_label.pack_forget()
        if self.badge2_label:
            self.badge2_label.pack_forget()
        if self.badge3_label:
            self.badge3_label.pack_forget()

# Create an instance of the PunchInPage class
app = PunchInPage()
# Start the tkinter event loop
app.mainloop()
>>>>>>> e10262d81f669a1b328b8d701cd09dc2fc306f00
