import sqlite3
import re
import tkinter as tk
from tkinter import messagebox

# Create the Customers table (you should also create other tables similarly)
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

def is_valid_email(email):
    # Define a regular expression pattern for a valid email address
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
    # Use the re.match() function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
    
def is_valid_phone_number(phone_number):
    # Remove any non-numeric characters (e.g., spaces, dashes, parentheses)
    cleaned_number = ''.join(filter(str.isdigit, phone_number))

    # Check if the cleaned phone number contains only digits
    if cleaned_number.isdigit():
        # Check if the length of the cleaned number is within an acceptable range
        if 7 <= len(cleaned_number) <= 15:
            return True
    return False

def add_customer(first_name_entry, last_name_entry, phone_number_entry, email_entry, listbox):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    # Check if the required fields are empty and if the phone number and email are valid
    if not first_name or not last_name:
        # Required fields are empty
        messagebox.showerror("Error", "First Name and Last Name are required fields.")
    elif not is_valid_phone_number(phone_number):
        # Phone number contains non-numeric characters
        messagebox.showerror("Error", "Phone Number must be valid.")
    elif not is_valid_email(email):
        # Email is not in a valid format
        messagebox.showerror("Error", "Invalid Email Address.")
    else:
        # All checks passed, add the customer to the database
        cursor.execute('''
            INSERT INTO Customers (first_name, last_name, phone_number, email)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, phone_number, email))
        connection.commit()
        refresh_customer_list(listbox)

        # Clear the entry widgets
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        phone_number_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Customer added successfully.")

# Function to edit a customer
def modify_customer(customer_listbox):

    # Get the selected item from the Listbox
    selected_index = customer_listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a customer to edit.")
        return

    # Extract the customer_id from the selected item
    customer_entry = customer_listbox.get(selected_index)

    try:
        customer_id = int(customer_entry.split("ID: ")[1].split(",")[0])
        existing_phone = customer_entry.split("Phone: ")[1].split(",")[0]
        existing_email = customer_entry.split("Email: ")[1].split(",")[0]
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract customer ID.")
        return
    
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Customer")# Create an edit dialog window
    
    # Create Entry widgets for the new phone and email
    phone_label = tk.Label(edit_window, text="New Phone:")
    phone_label.pack()
    new_phone_entry = tk.Entry(edit_window)
    new_phone_entry.insert(0, existing_phone)
    new_phone_entry.pack()

    email_label = tk.Label(edit_window, text="New Email:")
    email_label.pack()
    new_email_entry = tk.Entry(edit_window)
    new_email_entry.insert(0, existing_email)
    new_email_entry.pack()

    # Function to save changes and update the database
    def save_changes():
        new_phone = new_phone_entry.get()
        new_email = new_email_entry.get()

        if not is_valid_phone_number(new_phone):
            messagebox.showerror("Error", "Invalid Phone Number.")
            return

        if not is_valid_email(new_email):
            messagebox.showerror("Error", "Invalid Email Address.")
            return

        # Update the customer's phone and email in the database
        try:
            # Update the customer's phone and email in the database
            cursor.execute('''
                UPDATE Customers
                SET phone_number = ?, email = ?
                WHERE customer_id = ?
            ''', (new_phone, new_email, customer_id))

            # Commit the changes to the database
            connection.commit()
        except sqlite3.Error as e:
            print("Error updating customer phone and email:", e)
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
    for customer in customers:
        customer_info = f"ID: {customer[0]}, Name: {customer[1]} {customer[2]}, Phone: {customer[3]}, Email: {customer[4]}"
        listbox.insert(tk.END, customer_info)

