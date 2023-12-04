import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from regex_fcns import get_id

try:
    connection = sqlite3.connect("mechanic_shop.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vehicles (
            vin TEXT PRIMARY KEY,
            customer_id INTEGER,
            make TEXT,
            model TEXT,
            year INTEGER,
            FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
        )
    ''')
    connection.commit()
    # Create an index on the customer_id column
    # This improves performance when the appointments window searches for vehicles by customer_id
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS customer_id_index
        ON Vehicles(customer_id)
    ''')
    connection.commit()
    
    #Create a view on customers that have vehicles
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS customers_with_vehicles AS                      
            SELECT DISTINCT customers.customer_id, customers.first_name, customers.last_name                                        
            FROM Customers                                              
            JOIN vehicles ON customers.customer_id = vehicles.customer_id
    ''')
    connection.commit()

except sqlite3.Error as error:
    messagebox.showerror("Error", f"Error initialzing Vehicles table: {error}")
    connection.rollback()

def get_vehicles():
    try:
        cursor.execute('SELECT VIN, make, model FROM Vehicles')
        vehicles = cursor.fetchall()
        return vehicles
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error getting vehicles: {error}")

def customer_exists(customer_id):
    cursor.execute('''
        SELECT * FROM Customers WHERE customer_id = ?
    ''', (customer_id,))
    return cursor.fetchone()

def valid_vin(vin):
    if len(vin) != 17:
        return False
    if not vin.isalnum():
        return False
    return True

def vin_exists(vin):
    cursor.execute('''
        SELECT * FROM Vehicles WHERE vin = ?
    ''', (vin,))
    return cursor.fetchone()

def valid_year(year):
    if year < 1871 or year > datetime.now().year + 1: #first steam car-like vehicle invented in 1871 and 2024 cars exist in 2023
        return False
    return True

def add_vehicle(vin_entry, customer_id_entry, make_entry, model_entry, year_entry, vehicle_listbox):
    vin = vin_entry.get().upper()
    customer_id = customer_id_entry.get()
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()

    if not all((vin, customer_id, make, model, year)):
        # Required fields are empty
        messagebox.showerror("Error", "All fields are required.")
        return
    if not customer_exists(customer_id):
        # Customer ID does not exist
        messagebox.showerror("Error", "Customer ID does not exist.")
        return
    if not valid_vin(vin):
        # VIN is not valid
        messagebox.showerror("Error", "VIN is not valid. Must be of length 17.")
        return
    if vin_exists(vin):
        # VIN already exists
        messagebox.showerror("Error", "VIN already exists.")
        return
    try:
        cursor.execute('''
            INSERT INTO Vehicles (vin, customer_id, make, model, year)
            VALUES (?, ?, ?, ?, ?)
        ''', (vin, customer_id, make, model, year))
        connection.commit()
        refresh_vehicle_list(vehicle_listbox)

        for entry in (vin_entry, make_entry, model_entry, year_entry):
            entry.delete(0, tk.END)
        customer_id_entry.set("")
        messagebox.showinfo("Success", "Vehicle added successfully.")
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error adding vehicle: {error}")  

def modify_vehicle(vehicle_listbox):
    selected_index = vehicle_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a vehicle to edit.")
        return
    
    vehicle_entry = vehicle_listbox.get(selected_index)

    try:
        vin = (vehicle_entry.split("VIN: ")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract VIN.")
        return

    if not valid_vin(vin):
        messagebox.showerror("Error", "VIN is not valid. Must be of length 17.")
        return
    
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Vehicle")

    # Create Entry widgets for the new customer_id
    customer_id_label = tk.Label(
        edit_window,
        text="New Customer ID",
        fg="white",
    ).pack()
    new_customer_id_entry = tk.Entry(edit_window)
    new_customer_id_entry.pack()

    def save_changes():
        new_customer_id = new_customer_id_entry.get()

        if not customer_exists(new_customer_id):
            messagebox.showerror("Error", "Customer ID does not exist.")
            return
        try:
            cursor.execute('''
                UPDATE Vehicles
                SET customer_id = ?
                WHERE vin = ?
            ''', (new_customer_id, vin))
            connection.commit()
            refresh_vehicle_list(vehicle_listbox)
            messagebox.showinfo("Success", "Vehicle updated successfully.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error updating vehicle: {error}")
        refresh_vehicle_list(vehicle_listbox)
        edit_window.destroy()
    
    # Button to save changes
    save_button = tk.Button(edit_window, text="Save", command=save_changes).pack()
    
def refresh_vehicle_list(listbox):
    cursor.execute('''
        SELECT * FROM Vehicles
    ''')
    vehicles = cursor.fetchall()
    listbox.delete(0, tk.END)
    for vehicle in vehicles:
        vehicle_info = f"VIN: {vehicle[0]}, Customer ID: {vehicle[1]}, Make: {vehicle[2]}, Model: {vehicle[3]}, Year: {vehicle[4]}"
        listbox.insert(tk.END, vehicle_info)