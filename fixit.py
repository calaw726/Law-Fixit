import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from customer_functions import *


# Initialize the SQLite database
connection = sqlite3.connect('mechanic_shop.db')
cursor = connection.cursor()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x}+{y}')

def load_main_frame():
    # Create the main frame
    welcome_frame = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    welcome_frame.grid(row=0, column=0, sticky="nesw")
    welcome_frame.pack_propagate(False)

    # Create the logo
    logo_img = ImageTk.PhotoImage(get_logo())
    logo_widget = tk.Label(welcome_frame, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    # Create the buttons
    edit_tables_button = tk.Button(
        welcome_frame,
        text="Edit Tables",
        font=("Calibri", 48),
        fg="Black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda:load_edit_customer(),
        relief=tk.FLAT,
        borderwidth=0
    ).pack()

def load_edit_customer():
    edit_customer = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_customer.grid(row=0, column=0, sticky="nesw")
    edit_customer.pack_propagate(False)

    # Create input fields and buttons for managing customers
    first_name_label = tk.Label(
        edit_customer,
        text="First Name",
        bg = bg_color,
        fg="white",
        font=("Calibri", 12)
    )
    first_name_entry = tk.Entry(edit_customer)

    last_name_label = tk.Label(
        edit_customer,
        text="Last Name",
        bg = bg_color,
        fg="white",
        font=("Calibri", 12)
    )
    last_name_entry = tk.Entry(edit_customer)

    phone_number_label = tk.Label(
        edit_customer,
        text="Phone Number",
        bg=bg_color,
        fg="white",
        font=("Calibri", 12)
    )
    phone_number_entry = tk.Entry(edit_customer)

    email_label = tk.Label(
        edit_customer,
        text="Email",
        bg=bg_color,
        fg="white",
        font=("Calibri", 12)
    )
    email_entry = tk.Entry(edit_customer)

    add_button = tk.Button(
        edit_customer, 
        text="Add Customer",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: add_customer(
            first_name_entry,
            last_name_entry,
            phone_number_entry,
            email_entry,
            customer_listbox),
        relief=tk.FLAT,
        borderwidth=0

    )

    edit_button = tk.Button(
        edit_customer,
        text="Edit Customer",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: modify_customer(customer_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    button_row =tk.Frame(edit_customer, bg=bg_color)
    button_row.grid(row=1, column=0, sticky="nesw")
    button_row.pack(side=tk.BOTTOM)

    back_button = tk.Button(
        button_row,
        text="Back",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_main_frame(),
        relief=tk.FLAT,
        borderwidth=0
    )

    vehicles_button = tk.Button(
        button_row,
        text="Vehicles",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_edit_vehicle(),
        relief=tk.FLAT,
        borderwidth=0
    )

    services_button = tk.Button(
        button_row,
        text="Services",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_edit_service(),
        relief=tk.FLAT,
        borderwidth=0
    )

    appointments_button = tk.Button(
        button_row,
        text="Appointments",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_edit_appointment(),
        relief=tk.FLAT,
        borderwidth=0
    )

    invoices_button = tk.Button(
        button_row,
        text="Invoices",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_edit_invoice(),
        relief=tk.FLAT,
        borderwidth=0
    )

    # Create a listbox to display customers
    customer_listbox = tk.Listbox(edit_customer)
    customer_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Pack the input fields and buttons
    first_name_label.pack()
    first_name_entry.pack()
    last_name_label.pack()
    last_name_entry.pack()
    phone_number_label.pack()
    phone_number_entry.pack()
    email_label.pack()
    email_entry.pack()
    add_button.pack()
    edit_button.pack(padx=(10, 10))
    back_button.pack(side = "left", padx=10)
    vehicles_button.pack(side = "left", padx=10)
    services_button.pack(side = "left", padx=10)
    appointments_button.pack(side = "left", padx=10)
    invoices_button.pack(side = "left", padx=10)

    

    # Refresh the customer list
    refresh_customer_list(customer_listbox)


def get_logo():
    # Create the logo
    original_logo = Image.open(r'src/assets/logo.jpg')
    width, height = original_logo.size
    new_width = width // 2
    new_height = height // 2

    # Resize the logo
    resized_logo = original_logo.resize((new_width, new_height), Image.LANCZOS)
    return resized_logo

# Create the main window
bg_color = "#08142E"
button_color = "#1b4298"
button_pressed_color = "#becff4"

window_width = 800
window_height = 600

root = tk.Tk()
root.title("Law-Fixit DBMS")
center_window(root, window_width, window_height)
root.eval("tk::PlaceWindow . center")


load_main_frame()

# Start the Tkinter main loop
root.mainloop()
