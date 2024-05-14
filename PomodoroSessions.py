import sqlite3
from datetime import datetime

#Create database for Pomodoro
conn = sqlite3.connect('pomodoro.db')

#Cursor
cursor = conn.cursor ()

#Create Table
cursor.execute("""CREATE TABLE IF NOT EXISTS PomodoroSessions (
    SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
    User TEXT NOT NULL,
    Mode TEXT NOT NULL,
    SessionType TEXT NOT NULL,
    Duration INTEGER NOT NULL,
    CompletionTime TEXT NOT NULL
);
""")


def insert_pomodoro_session(mode, session_type, duration, user='John'):
    conn = sqlite3.connect('pomodoro.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    
    completion_time = datetime.now().isoformat()  # Get the current completion time
    
    # Execute the SQL query to insert the session into the table
    cursor.execute('''
    INSERT INTO PomodoroSessions (User, Mode, SessionType, Duration, CompletionTime)
    VALUES (?, ?, ?, ?, ?)
    ''', (user, mode, session_type, duration, completion_time))
    
    conn.commit()  # Commit the transaction
    conn.close() 
