import tkinter as tk
from tkinter import ttk
import calendar

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

        # Add title label
        self.title_label = tk.Label(title_frame, text="My Achievement", font=("Cooper Black", 50, "bold"), background="light yellow")
        self.title_label.pack(pady=(10, 0))

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

            self.punch_status[punched_date] = True  # Mark as punched
            punch_box.config(bg="bisque3")  # Change background color to indicate punched

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