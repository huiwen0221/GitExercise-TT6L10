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
durations = np.random.randint(15, 30, size=len(date_range))  # Duration between 15 to 30 minutes
data = {
    "Start": date_range,
    "Duration": durations
}
df = pd.DataFrame(data)
df.set_index('Start', inplace=True)

class StatisticsApp:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Statistics")
        # Add a Button to Generate Statistics
        self.stats_button = ttk.Button(master, text="Show Statistics", command=self.show_stats)
        self.stats_button.pack(pady=10)

        # Frame for Matplotlib Figure
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

    def show_stats(self):
    # Compute summary data
     weekly = df.resample('W').sum()
     monthly = df.resample('M').sum()
    
    # Rename the index to week numbers and month names
     weekly.index = ["Week " + str(i+1) for i in range(len(weekly))]
     monthly.index = monthly.index.strftime('%B')  # Formats the datetime index to month names

    # Plotting
     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
     weekly['Duration'].plot(ax=ax1, title='Weekly Pomodoro Minutes', kind='bar', color='blue')
     monthly['Duration'].plot(ax=ax2, title='Monthly Pomodoro Minutes', kind='bar', color='green')

    # Embedding Plot in Tkinter
     canvas = FigureCanvasTkAgg(fig, master=self.frame)
     canvas.draw()
     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = StatisticsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

