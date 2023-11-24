import sqlite3
import tkinter as tk
from tkinter import ttk
import string
from tkinter import messagebox
from tkcalendar import Calendar
from time_utils import *

# Create the Appointments table
connection = sqlite3.connect('mechanic_shop.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        appointment_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        vehicle_id TEXT,
        service_id INTEGER,
        appointment_date TEXT,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
        FOREIGN KEY (service_id) REFERENCES Services(service_id)
    )
''')
connection.commit()

def get_services():
    cursor.execute('''
        SELECT service_id, service_name FROM Services
    ''')
    services = cursor.fetchall()
    return services

def get_vehicle_ids(customer_id):
    cursor.execute('''
        SELECT VIN FROM Vehicles WHERE customer_id = ?
    ''', (customer_id,))
    vehicle_ids = [row[0] for row in cursor.fetchall()]
    return vehicle_ids

def appointment_exists(appointment_id):
    cursor.execute('''
        SELECT * FROM Appointments WHERE appointment_id = ?
    ''', (appointment_id,))
    return cursor.fetchone()

def customer_exists(customer_id):
    cursor.execute('''
        SELECT * FROM Customers WHERE customer_id = ?
    ''', (customer_id,))
    return cursor.fetchone()

def service_exists(service_id):
    cursor.execute('''
        SELECT * FROM Services WHERE service_id = ?
    ''', (service_id,))
    return cursor.fetchone()

def remove_punctuation(in_string):
    translation_table = str.maketrans("", "", string.punctuation)

    result = in_string.translate(translation_table)

    return result

def add_appointment(listbox, customer_id_entry, vehicle_id_entry, service_id_entry, appointment_date_entry, status_entry):
    customer_id = customer_id_entry.get()
    vehicle_id = remove_punctuation(vehicle_id_entry.get())
    service_id = service_id_entry.get()[0]
    appointment_date = appointment_date_entry.get()
    status = status_entry.get()
    # Check if the required fields are empty
    if not all((customer_id, vehicle_id, service_id, appointment_date, status)):
        # Required fields are empty
        messagebox.showerror("Error", "All fields are required.")
        return
    if not customer_exists(customer_id):
        # Customer ID does not exist
        messagebox.showerror("Error", "Customer ID does not exist.")
        return
    if not service_exists(service_id):
        # Service ID does not exist
        messagebox.showerror("Error", "Service ID does not exist.")
        return
    try:
        cursor.execute('''
            INSERT INTO Appointments (customer_id, vehicle_id, service_id, appointment_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, vehicle_id, service_id, appointment_date, status))
        connection.commit()
        refresh_appointment_list(listbox)

        # Clear the entry widgets
        for entry in (customer_id_entry, appointment_date_entry):
            entry.delete(0, tk.END)
        vehicle_id_entry.set("")
        service_id_entry.set("")
        status_entry.set("")
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error adding appointment: {error}")

def modify_appointment(listbox):
    selected_index = listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select an appointment to modify.")
        return
    
    appointment_entry = listbox.get(selected_index)

    try:
        appointment_id = int(appointment_entry.split("ID: ")[1].split(",")[0])
        existing_customer_id = int(appointment_entry.split("Customer ID: ")[1].split(",")[0])
        existing_vehicle_id = (appointment_entry.split("Vehicle ID: ")[1].split(",")[0])
        existing_service_id = int((appointment_entry.split("Service ID: ")[1].split(",")[0])[0])
        existing_appointment_date = (appointment_entry.split("Date: ")[1].split(",")[0])
        existing_status = (appointment_entry.split("Status: ")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract appointment ID.")
        return
    
    if not customer_exists(existing_customer_id):
        messagebox.showerror("Error", "Customer ID does not exist.")
        return
    if not service_exists(existing_service_id):
        messagebox.showerror("Error", "Service ID does not exist.")
        return
    if not appointment_exists(appointment_id):
        messagebox.showerror("Error", "Appointment ID is not valid.")
        return
    
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Appointment")

    vin_label = tk.Label(edit_window, text="Vehicle ID:")
    vin_label.pack()

    vehicle_var = tk.StringVar()
    vehicle_combobox = ttk.Combobox(edit_window, textvariable=vehicle_var)
    vehicle_combobox['values'] = get_vehicle_ids(existing_customer_id)
    vehicle_combobox.set(existing_vehicle_id)
    vehicle_combobox.pack()

    service_label = tk.Label(edit_window, text="Service ID:")
    service_label.pack()

    service_var = tk.StringVar()
    services_combobox = ttk.Combobox(edit_window, textvariable=service_var)
    services_combobox['values'] = get_services()
    services_combobox.set(existing_service_id)
    services_combobox.pack()

    calendar = Calendar(edit_window, selectmode="day")
    calendar.pack(pady=20)

    date_entry = tk.Entry(edit_window, width=12, background="darkblue", foreground="white", borderwidth=2)
    date_entry.pack(pady=20)
    date_entry.insert(0, existing_appointment_date)

    time_label = tk.Label(edit_window, text="Time:")
    time_label.pack()

    time_frame = tk.Frame(edit_window)
    time_frame.pack()

    hour_spinbox = tk.Spinbox(time_frame, from_=8, to=16, width=2)
    hour_spinbox.grid(row=0, column=0)
    colon_label = tk.Label(time_frame, text=":")
    colon_label.grid(row=0, column=1)
    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2)
    minute_spinbox.grid(row=0, column=2)

    get_datetime_button = tk.Button(
        edit_window,
        text="Get Date and Time",
        command=lambda: get_selected_date(calendar, date_entry, hour_spinbox, minute_spinbox, False)
    )
    get_datetime_button.pack(pady=20)


    status_label = tk.Label(edit_window, text="Status:")
    status_label.pack()

    status_var = tk.StringVar()
    status_combobox = ttk.Combobox(edit_window, textvariable=status_var)
    status_combobox['values'] = ["Pending", "In Progress", "Complete"]
    status_combobox.set(existing_status)
    status_combobox.pack()

    # Create Entry widgets for the new vehicle_id, service_id, appointment_date, and status

    def save_changes():
        new_vehicle_id = vehicle_var.get()
        new_service_id = service_var.get()[0]
        new_appointment_date = date_entry.get()
        new_status = status_var.get()

        if not all((new_vehicle_id, new_service_id, new_appointment_date, new_status)):
            messagebox.showerror("Error", "All fields are required.")
            return
        if not service_exists(new_service_id):
            messagebox.showerror("Error", "Service ID does not exist.")
            return

        try:
            cursor.execute('''
                UPDATE Appointments
                SET vehicle_id = ?, service_id = ?, appointment_date = ?, status = ?
                WHERE appointment_id = ?
            ''', (new_vehicle_id, new_service_id, new_appointment_date, new_status, appointment_id))
            connection.commit()
            refresh_appointment_list(listbox)
            messagebox.showinfo("Success", "Appointment updated successfully.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error updating appointment: {error}")
        refresh_appointment_list(listbox)
        edit_window.destroy()
    
    # Button to save changes
    save_button = tk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack()

def delete_appointment(listbox):
    selected_index = listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select an appointment to delete.")
        return
    
    appointment_entry = listbox.get(selected_index)

    try:
        appointment_id = int(appointment_entry.split("ID: ")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract appointment ID.")
        return
    
    if not appointment_exists(appointment_id):
        messagebox.showerror("Error", "Appointment ID is not valid.")
        return
    
    try:
        cursor.execute('''
            DELETE FROM Appointments
            WHERE appointment_id = ?
        ''', (appointment_id,))
        connection.commit()
        refresh_appointment_list(listbox)
        messagebox.showinfo("Success", "Appointment deleted successfully.")
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error deleting appointment: {error}")

def refresh_appointment_list(listbox):
    listbox.delete(0, tk.END)
    cursor.execute('''
        SELECT * FROM Appointments
    ''')
    for row in cursor.fetchall():
        appointment_info = f"ID: {row[0]}, Customer ID: {row[1]}, Vehicle ID: {row[2]}, Service ID: {row[3]}, Date: {row[4]}, Status: {row[5]}"
        listbox.insert(tk.END, appointment_info)