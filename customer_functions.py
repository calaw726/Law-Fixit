import sqlite3
import re
import tkinter as tk
from tkinter import messagebox, ttk

# Define a regular expression pattern for a valid email address
EMAIL_PATTERN = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

# Create the Customers table
try:
    connection = sqlite3.connect('mechanic_shop.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            email TEXT
        )
    ''')
    connection.commit()
except sqlite3.Error as error:
    messagebox.showerror("Error", f"Error initializing Customers table: {error}")
    connection.rollback()

def is_valid_email(email):    
    # Use the re.match() function to check if the email matches the pattern
    return bool(EMAIL_PATTERN.fullmatch(email))
    
def is_valid_phone_number(phone_number):
    # Ensure the phone number is a string
    if not isinstance(phone_number, str):
        return False
    
    # Remove any non-numeric characters (e.g., spaces, dashes, parentheses)
    cleaned_number = ''.join(filter(str.isdigit, phone_number))

    # Check if the cleaned phone number contains only digits and is between 7 and 15 digits long
    return cleaned_number.isdigit() and 7 <= len(cleaned_number) <= 15

def list_customers(customer_var, customer_combobox):
    try:
        cursor.execute('SELECT customer_id, first_name, last_name FROM Customers')
        customers = cursor.fetchall()
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error retrieving customers: {error}")
        return
    
    # Clear the Combobox
    customer_combobox.set("")
    customer_combobox['values'] = ()

    if not customers:
        messagebox.showerror("Error", "No customers found.")
        return
    # Extract the customer names from the list of customers
    customer_values = [f"{id}: {first_name} {last_name}" for id, first_name, last_name in customers]

    # Set the Combobox values
    customer_combobox['values'] = customer_values

    # Function to set the selected customer in the variable
    def set_customer(event):
        index = customer_combobox.current()
        if index >= 0:
            customer_id = customers[index][0]
            customer_var.set(customer_id)

    # Bind the set_customer function to the Combobox
    customer_combobox.bind("<<ComboboxSelected>>", set_customer)

def add_customer(first_name_entry, last_name_entry, phone_number_entry, email_entry, listbox):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    # Check if the required fields are empty and if the phone number and email are valid
    if not first_name or not last_name:
        # Required fields are empty
        messagebox.showerror("Error", "First Name and Last Name are required fields.")
        return
    if not is_valid_phone_number(phone_number):
        # Phone number contains non-numeric characters
        messagebox.showerror("Error", "Phone Number must be valid.")
        return
    if not is_valid_email(email):
        # Email is not in a valid format
        messagebox.showerror("Error", "Invalid Email Address.")
        return
    try:
        cursor.execute('''
            INSERT INTO Customers (first_name, last_name, phone_number, email)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, phone_number, email))
        connection.commit()
        refresh_customer_list(listbox)

        # Clear the entry widgets
        for entry in (first_name_entry, last_name_entry, phone_number_entry, email_entry):
            entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Customer added successfully.")
    except sqlite3.Error as error:
        connection.rollback()
        messagebox.showerror("Error", f"Error adding customer: {error}")

# Function to edit a customer
def modify_customer(customer_listbox):

    # Get the selected item from the Listbox
    selected_index = customer_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a customer to edit.")
        return
    
    try:
        # Extract the customer_id from the selected item
        customer_entry = customer_listbox.get(selected_index)
        _, customer_id = re.search(r'ID: (\d+)', customer_entry).groups()
        existing_phone = re.search(r'Phone: (.*?),', customer_entry).group(1)
        existing_email = re.search(r'Email: (.*?),', customer_entry).group(1)
    except (AttributeError):
        messagebox.showerror("Error", "Unable to extract customer ID.")
        return
    
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Customer")# Create an edit dialog window
    
    # Create Entry widgets for the new phone and email
    entries_and_labels = [
        ("New Phone:", existing_phone),
        ("New Email:", existing_email)
    ]
    entry_values = []

    for label_text, default_value in entries_and_labels:
        label = tk.Label(edit_window, text=label_text)
        label.pack()

        entry = tk.Entry(edit_window)
        entry.insert(0, default_value)
        entry.pack()
        entry_values.append(entry)

    # Function to save changes and update the database
    def save_changes():
        new_phone = entry_values[0].get()
        new_email = entry_values[1].get()

        if not is_valid_phone_number(new_phone):
            messagebox.showerror("Error", "Invalid Phone Number.")
            return

        if not is_valid_email(new_email):
            messagebox.showerror("Error", "Invalid Email Address.")
            return

        # Update the customer's phone and email in the database
        try:
            cursor.execute('''
                UPDATE Customers
                SET phone_number = ?, email = ?
                WHERE customer_id = ?
            ''', (new_phone, new_email, customer_id))

            # Commit the changes to the database
            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            print("Error updating customer phone and email:", e)
            return

        edit_window.destroy()
        refresh_customer_list(customer_listbox)
        messagebox.showinfo("Success", "Customer updated successfully.")

    # Button to save changes
    save_button = tk.Button(edit_window, text="Save", command=save_changes)
    save_button.pack()

    refresh_customer_list(customer_listbox)

# Function to refresh the customer list
def refresh_customer_list(listbox):
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()

    listbox.delete(0, tk.END)

    # Use a list comprehension for constructing customer_info strings
    customer_infos = [
        f"ID: {customer[0]}, Name: {customer[1]} {customer[2]}, Phone: {customer[3]}, Email: {customer[4]}"
        for customer in customers
    ]
    
    for customer_info in customer_infos:
        listbox.insert(tk.END, customer_info)

