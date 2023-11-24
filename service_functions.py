import sqlite3
import tkinter as tk
from tkinter import messagebox

connection = sqlite3.connect("mechanic_shop.db")
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Services (
        service_id INTEGER PRIMARY KEY,
        service_name TEXT,
        description TEXT,
        price REAL
    )
''')
connection.commit()

def valid_service_id(service_id):
    if not service_id.isdigit():
        return False
    return True

def valid_price(price):
    try:
        float(price)
    except ValueError:
        return False
    return True

def add_service(service_listbox, service_name_entry, description_entry, price_entry):
    service_name = service_name_entry.get()
    description = description_entry.get()
    price = price_entry.get()

    # Check if the required fields are empty
    if not all((service_name, description, price)):
        # Required fields are empty
        messagebox.showerror("Error", "All fields are required.")
        return
    if not valid_price(price):
        # Invalid price
        messagebox.showerror("Error", "Invalid price. Must be a number")
        return
    try:
        cursor.execute('''
            INSERT INTO Services (service_name, description, price)
            VALUES (?, ?, ?)
        ''', (service_name, description, price))
        connection.commit()

    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error adding Service: {error}.")

    # Refresh the service list
    refresh_service_list(service_listbox)

    # Clear the entry widgets
    for entry in (service_name_entry, description_entry, price_entry):
        entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Service added successfully.")

def modify_service(service_listbox):
    # Get the currently selected service from the listbox
    selected_index = service_listbox.curselection()

    if not selected_index:
        # No service is selected
        messagebox.showerror("Error", "Please select a service to modify.")
        return
    service_entry = service_listbox.get(selected_index)

    try:
        service_id = int(service_entry.split("ID: ")[1].split(",")[0])
        existing_service_name = (service_entry.split("Name: ")[1].split(",")[0])
        existing_price = float(service_entry.split("Price: $")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract service ID.")
        return
    
    try:
        existing_description = cursor.execute('''
            SELECT description FROM Services
            WHERE service_id = ?
        ''', (service_id,)).fetchone()[0]
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error getting description: {error}.")
        return
    
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Service")

    # Create Entry widgets for the new service name, description, and price
    labels_and_entries = [
        ("Service Name:", existing_service_name),
        ("Description:", existing_description),
        ("Price:", existing_price)
    ]

    entry_values = []

    for label, default_value in labels_and_entries:
        tk.Label(edit_window, text=label).pack()
        entry = tk.Entry(edit_window)
        entry.insert(0, default_value)
        entry.pack()
        entry_values.append(entry)

    def save_changes():
        new_service_name = entry_values[0].get()
        new_description = entry_values[1].get()
        new_price = entry_values[2].get()

        if not all ((new_service_name, new_description, new_price)):
            messagebox.showerror("Error", "All fields are required.")
            return
        if not valid_price(new_price):
            # Invalid price
            messagebox.showerror("Error", "Invalid price. Must be a number")
            return
        try:
            cursor.execute('''
                UPDATE Services
                SET service_name = ?, description = ?, price = ?
                WHERE service_id = ?
            ''', (new_service_name, new_description, new_price, service_id))
            connection.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error updating service: {error}.")
        edit_window.destroy()
        refresh_service_list(service_listbox)

    # Create a button to save the changes
    save_button = tk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack()
    

def delete_service(service_listbox):
    selected_index = service_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a service to delete.")
        return

    try:
        # Extract the service ID from the selected listbox entry
        service_entry = service_listbox.get(selected_index)
        service_id = (service_entry.split("ID: ")[1].split(",")[0])

        # Delete the service from the database
        cursor.execute('''
            DELETE FROM Services
            WHERE service_id = ?
        ''', (service_id,))
        connection.commit()
        refresh_service_list(service_listbox)
    except (ValueError, IndexError, sqlite3.Error) as error:
        messagebox.showerror("Error", f"Error deleting service: {error}.")
    
    

def get_description(service_listbox):
    selected_index = service_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a service to get description.")
        return
    
    service_entry = service_listbox.get(selected_index)

    try:
        service_id = (service_entry.split("ID: ")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract service ID.")
        return
    
    try:
        cursor.execute('''
            SELECT description FROM Services
            WHERE service_id = ?
        ''', (service_id,))
        connection.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error getting description: {error}.")
    description = cursor.fetchone()[0]
    messagebox.showinfo("Description", description)


def refresh_service_list(service_listbox):
    cursor.execute("""
        SELECT * FROM Services
    """)
    services = cursor.fetchall()
    service_listbox.delete(0, tk.END)
    for service in services:
        service_info = f"ID: {service[0]}, Name: {service[1]}, Price: ${service[3]}"
        service_listbox.insert(tk.END, service_info)



