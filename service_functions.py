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

def add_service(service_listbox, service_name_entry, description_entry, price_entry):
    service_name = service_name_entry.get()
    description = description_entry.get()
    price = price_entry.get()

    # Check if the required fields are empty
    if not service_name or not description or not price:
        # Required fields are empty
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        cursor.execute('''
            INSERT INTO Services (service_name, description, price)
            VALUES (?, ?, ?)
        ''', (service_name, description, price))
        connection.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error adding Service: {error}.")
    refresh_service_list(service_listbox)

    # Clear the entry widgets
    service_name_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

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
    service_name_label = tk.Label(edit_window, text="Service Name:")
    service_name_entry = tk.Entry(edit_window)
    service_name_entry.insert(0, existing_service_name)
    description_label = tk.Label(edit_window, text="Description:")
    description_entry = tk.Entry(edit_window)
    description_entry.insert(0, existing_description)
    price_label = tk.Label(edit_window, text="Price:")
    price_entry = tk.Entry(edit_window)
    price_entry.insert(0, existing_price)

    # Pack the widgets
    service_name_label.pack()
    service_name_entry.pack()
    description_label.pack()
    description_entry.pack()
    price_label.pack()
    price_entry.pack()

    def save_changes():
        new_service_name = service_name_entry.get()
        new_description = description_entry.get()
        new_price = price_entry.get()

        if not new_service_name or not new_description or not new_price:
            messagebox.showerror("Error", "All fields are required.")
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

    # Create a button to save the changes
    save_button = tk.Button(edit_window, text="Save", command=save_changes).pack()
    refresh_service_list(service_listbox)

def delete_service(service_listbox):
    selected_index = service_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a service to delete.")
        return
    service_entry = service_listbox.get(selected_index)

    try:
        service_id = (service_entry.split("ID: ")[1].split(",")[0])
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract service ID.")
        return

    try:
        cursor.execute('''
            DELETE FROM Services
            WHERE service_id = ?
        ''', (service_id,))
        connection.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error deleting service: {error}.")
    refresh_service_list(service_listbox)

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



