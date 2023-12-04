import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from time_utils import get_curr_date

# Create the Invoices table
try:
    connection = sqlite3.connect('mechanic_shop.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invoices (
            invoice_id INTEGER PRIMARY KEY,
            appointment_id INTEGER,
            total_cost REAL,
            payment_status TEXT,
            date_paid TEXT,
            FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id)
        )
    ''')
    connection.commit()
except sqlite3.Error as error:
    connection.rollback()
    messagebox.showerror("Error", f"Error creating Invoices table: {error}")

def appointment_exists(appointment_id):
    cursor.execute('''
        SELECT * FROM Appointments
        WHERE appointment_id = ?
    ''', (appointment_id,))
    return bool(cursor.fetchone() is not None)

def add_invoice(appointment_id_entry, total_cost_entry, payment_status_entry, date_paid_entry, listbox):
    appointment_id = appointment_id_entry.get()
    total_cost = total_cost_entry.get()
    payment_status = payment_status_entry.get()
    date_paid = date_paid_entry.get()

    # Check if the required fields are empty
    if not all((appointment_id, total_cost, payment_status)):
        messagebox.showerror("Error", "Appointment ID, Total Cost, and Payment Status are required fields.")
        return
    if not appointment_exists(appointment_id):
        messagebox.showerror("Error", "Provided Appointment ID does not exist.")
        return
    try:
        cursor.execute('''
            INSERT INTO Invoices (appointment_id, total_cost, payment_status, date_paid)
            VALUES (?, ?, ?, ?)
        ''', (appointment_id, total_cost, payment_status, date_paid))
        connection.commit()
        refresh_invoice_list(listbox)

        # Clear the entry fields
        appointment_id_entry.delete(0, tk.END)
        total_cost_entry.delete(0, tk.END)
        payment_status_entry.delete(0, tk.END)
        date_paid_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        connection.rollback()
        messagebox.showerror("Error", "Appointment ID must be unique.")
        return
    
def modify_invoice(listbox):
    # Get the selected item from the listbox
    selected_index = listbox.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select an invoice to modify.")
        return
    try:
        # Get the invoice ID from the selected item
        invoice_entry = listbox.get(selected_index)
        invoice_id = int(invoice_entry.split("ID: ")[1].split(",")[0])
        existing_payment_status = invoice_entry.split("Payment Status: ")[1].split(",")[0]
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Unable to extract invoice ID.")
        return
    # Create an edit dialog window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Invoice")

    # Create the label
    payment_status_label = tk.Label(edit_window, text="Payment Status:")
    payment_status_label.pack()

    # Create the dropdown box
    status_var = tk.StringVar()
    status_var.set(existing_payment_status)
    status_options = ["Paid", "Unpaid"]
    status_combobox = ttk.Combobox(edit_window, textvariable=status_var, values=status_options)
    status_combobox.set(existing_payment_status)
    status_combobox.pack()

    def save_changes():
        payment_status = status_var.get()

        try:
            if payment_status == "Paid":
                cursor.execute('''
                    UPDATE Invoices
                    SET payment_status = ?, date_paid = ?
                    WHERE invoice_id = ?
                ''', (payment_status, get_curr_date(), invoice_id))
            else:
                cursor.execute('''
                    UPDATE Invoices
                    SET payment_status = ?, date_paid = NULL
                    WHERE invoice_id = ?
                ''', (payment_status, invoice_id))
            connection.commit()
            refresh_invoice_list(listbox)
        except sqlite3.Error as error:
            connection.rollback()
            messagebox.showerror("Error", f"Error updating invoice: {error}")
        edit_window.destroy()
    
    # Button to save changes
    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack()


def refresh_invoice_list(listbox):
    listbox.delete(0, tk.END)
    cursor.execute('''
        SELECT * FROM Invoices
    ''')
    for invoice in cursor.fetchall():
        invoice_info = f"ID: {invoice[0]}, Appointment ID: {invoice[1]}, Total Cost: {invoice[2]}, Payment Status: {invoice[3]}, Date Paid: {invoice[4]}"
        listbox.insert(tk.END, invoice_info)