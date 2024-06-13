import tkinter as tk
from PIL import Image, ImageTk
import time

class Page(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Tracker")
        
        self.time_started = None
        self.total_time = 0
        self.badge_awarded = False
        
        self.label = tk.Label(self, text="Click 'Start' to begin tracking time")
        self.label.pack(pady=20)
        
        self.start_button = tk.Button(self, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.time_label = tk.Label(self, text="Total time: 0 seconds")
        self.time_label.pack(pady=5)
        
        # Load badge image
        self.badge_image = Image.open(file="badge1.png")  # Replace "badge_image.png" with the path to your badge image
        self.badge_image = self.badge_image.resize((50, 50), Image.ANTIALIAS)  # Resize image
        self.badge_image = ImageTk.PhotoImage(self.badge_image)
        
        self.badge_label = tk.Label(self, image=self.badge_image)
        self.badge_label.pack(pady=5)
        
        self.badge_label.config(text="")
        
        self.target_time = 10  # Set the target time for badge in seconds
        
    def start_timer(self):
        self.time_started = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()
        
    def stop_timer(self):
        if self.time_started is not None:
            self.total_time += time.time() - self.time_started
            self.time_started = None
            self.update_timer()
            if self.total_time >= self.target_time and not self.badge_awarded:
                self.label.config(text="Congratulations! You've achieved the target time.")
                self.badge_label.config(text="Badge awarded!")
                self.badge_awarded = True
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
    def update_timer(self):
        if self.time_started is not None:
            current_time = time.time()
            elapsed_time = current_time - self.time_started
            self.time_label.config(text="Total time: {} seconds".format(int(self.total_time + elapsed_time)))
            self.after(1000, self.update_timer)
        else:
            self.time_label.config(text="Total time: {} seconds".format(int(self.total_time)))

if __name__ == "__main__":
    app = Page()
    app.mainloop()
