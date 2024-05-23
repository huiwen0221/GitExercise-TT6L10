import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import sqlite3
import random

class StatisticsApp:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Statistics")

        #Buttons for weekly and monthly data
        self.weekly_button = tk.Button(master, text="Show Weekly", command=self.show_weekly)
        self.weekly_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.monthly_button = tk.Button(master, text="Show Monthly", command=self.show_monthly)
        self.monthly_button.pack(side=tk.LEFT, padx=10, pady=10)

        #Frame for graph
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.current_plot = None  #Keep track of current plot

        self.create_database()
        self.insert_sample_data()

    def create_database(self):
        self.conn = sqlite3.connect('pomodorohelper.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PomodoroSessions (
            SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
            User TEXT NOT NULL,
            Mode TEXT NOT NULL,
            SessionType TEXT NOT NULL,
            Duration INTEGER NOT NULL,
            BreakDuration INTEGER NOT NULL,
            TimerDuration INTEGER NOT NULL,
            CompletionTime TEXT NOT NULL
        );""")
        self.conn.commit()

    def insert_sample_data(self):
        user = "John"
        modes = ["Default", "Study", "Relax"]

        #Data for 30 days
        for _ in range(100):
            mode = random.choice(modes)
            if mode in ["Default", "Study"]:
                duration = random.randint(15, 30)
                session_type = "Short Break" if duration < 16 else "Long Break" #15 min is short break
                break_duration = 0
                timer_duration = duration
            else:  #Relax mode
                duration = random.randint(5, 10)
                session_type = "Short Break" if duration < 11 else "Long Break" #10 min is long break
                break_duration = duration
                timer_duration = 0
            completion_time = (datetime.now() - timedelta(days=random.randint(0, 30),
                                                          hours=random.randint(0, 23),
                                                          minutes=random.randint(0, 59))).isoformat()

            self.cursor.execute('''
                INSERT INTO PomodoroSessions (User, Mode, SessionType, Duration, BreakDuration, TimerDuration, CompletionTime)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user, mode, session_type, duration, break_duration, timer_duration, completion_time))

        self.conn.commit()

    def show_weekly(self):
        self.cursor.execute('''
            SELECT strftime('%w', CompletionTime) AS Weekday, 
                   SUM(BreakDuration) AS BreakDuration, 
                   SUM(TimerDuration) AS TimerDuration 
            FROM PomodoroSessions 
            GROUP BY Weekday
        ''')
        weekly_data = self.cursor.fetchall()
        weekdays_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekly = pd.DataFrame(weekly_data, columns=['Weekday', 'Break Duration', 'Timer Duration'])
        weekly['Weekday'] = weekly['Weekday'].astype(int).apply(lambda x: weekdays_order[x])
        weekly.set_index('Weekday', inplace=True)
        weekly['Break Duration'] /= 60 
        weekly['Timer Duration'] /= 60  
        self.plot_statistics(weekly, x_label='Weekday', y_label='Duration (hours)')

    def show_monthly(self):
        self.cursor.execute('''
            SELECT strftime('%Y-%m', CompletionTime) AS MonthStart, 
                   SUM(BreakDuration) AS BreakDuration, 
                   SUM(TimerDuration) AS TimerDuration 
            FROM PomodoroSessions 
            GROUP BY MonthStart
        ''')
        monthly_data = self.cursor.fetchall()
        monthly = pd.DataFrame(monthly_data, columns=['MonthStart', 'Break Duration', 'Timer Duration'])
        monthly.set_index('MonthStart', inplace=True)
        monthly['Break Duration'] /= 60  
        monthly['Timer Duration'] /= 60  
        self.plot_statistics(monthly, x_label='Month Start', y_label='Duration (hours)')

    def plot_statistics(self, data, x_label, y_label):
        #Clear the current plot if exists
        if self.current_plot:
            self.current_plot.get_tk_widget().pack_forget()
            self.current_plot = None
        fig, ax = plt.subplots(figsize=(10, 6))
        #Break duration
        ax.bar(data.index, data['Break Duration'], label='Break', color='blue', alpha=0.5)
        #Timer duration
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
