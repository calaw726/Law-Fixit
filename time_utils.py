from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def get_selected_date(calendar, date_entry, hour_spinbox, minute_spinbox, check):
    # Get selected date from the calendar
    selected_date_str = calendar.get_date()

    # Parse the selected date string
    selected_date = datetime.strptime(selected_date_str, "%m/%d/%y")

    if check:
        if selected_date < datetime.now():
            messagebox.showerror("Error", "You cannot select a date in the past!")
            return

    # Get selected time from the Spinboxes
    if hour_spinbox and minute_spinbox:
        selected_hour = int(hour_spinbox.get())
        selected_minute = int(minute_spinbox.get())

        # Combine date and time in the desired format (MM/DD/YYYY HH:MM)
        formatted_date = selected_date.strftime('%m/%d/%Y')
        selected_datetime = f"{formatted_date} {selected_hour:02d}:{selected_minute:02d}"
    else:
        # Combine date and time in the desired format (MM/DD/YYYY)
        selected_datetime = selected_date.strftime('%m/%d/%Y')
    
    # Update the date entry widget
    date_entry.delete(0, tk.END)
    date_entry.insert(0, selected_datetime)

        

def format_date_time(date_time):
    formatted_date = datetime.strptime(date_time, "%Y-%m-%d").strftime("%d/%m/%Y %H:%M")
    return formatted_date

def get_curr_date():
    return datetime.now().strftime('%m/%d/%Y')