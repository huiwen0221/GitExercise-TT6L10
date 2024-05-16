import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

# Setup realistic random data
np.random.seed(0)
date_range = pd.date_range(start=datetime.now() - timedelta(days=30), periods=60, freq='2H')
break_durations = np.random.randint(3, 10, size=len(date_range))  # Break duration between 3 to 10 minutes
timer_durations = np.random.randint(15, 30, size=len(date_range))  # Timer duration between 15 to 30 minutes
data = {
    "Start": date_range,
    "Break Duration": break_durations,
    "Timer Duration": timer_durations
}
df = pd.DataFrame(data)
df.set_index('Start', inplace=True)

class StatisticsApp:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Statistics")
        # Add Buttons to Show Weekly and Monthly Statistics
        self.weekly_button = ttk.Button(master, text="Show Weekly", command=self.show_weekly)
        self.weekly_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.monthly_button = ttk.Button(master, text="Show Monthly", command=self.show_monthly)
        self.monthly_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame for Matplotlib Figure
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.current_plot = None  #keep track current plot

    def show_weekly(self):
        df['Weekday'] = df.index.strftime('%A')
        weekly = df.groupby('Weekday').sum()
        weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly = weekly.reindex(weekdays_order)
        weekly['Break Duration'] /= 60
        weekly['Timer Duration'] /= 60
        self.plot_statistics(weekly, x_label='Weekday', y_label='Duration (hours)')

    def show_monthly(self):
        df['WeekNumber'] = df.index.to_period('W-MON').strftime('Week %W')
        monthly = df.groupby('WeekNumber').sum()
        monthly['Break Duration'] /= 60
        monthly['Timer Duration'] /= 60
        self.plot_statistics(monthly, x_label='Week Number', y_label='Duration (hours)')

    def plot_statistics(self, data,x_label,y_label):
        # Clear the current plot if exists
        if self.current_plot:
            self.current_plot.get_tk_widget().pack_forget()
            self.current_plot = None
        fig, ax = plt.subplots(figsize=(10, 6))
        # Plotting Break Duration
        ax.bar(data.index, data['Break Duration'], label='Break', color='blue', alpha=0.5)
        # Plotting Timer Duration
        ax.bar(data.index, data['Timer Duration'], bottom=data['Break Duration'], label='Timer', color='orange', alpha=0.5)
        ax.set_title('Pomodoro Statistics')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.current_plot = canvas

def main():
    root = tk.Tk()
    app = StatisticsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
