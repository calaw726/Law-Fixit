import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from customer_functions import *
from vehicle_functions import *
from service_functions import *


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
        font=(font_family, 48),
        fg="Black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda:load_edit_customer(),
        relief=tk.FLAT,
        borderwidth=0
    ).pack()

    center_window(root, window_width, window_height)

def load_edit_customer():
    edit_customer = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_customer.grid(row=0, column=0, sticky="nesw")
    edit_customer.pack_propagate(False)

    # Create a listbox to display customers
    customer_listbox = tk.Listbox(edit_customer)
    customer_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Labels and Entries
    labels_and_entries = [
        ("First Name:", tk.Entry(edit_customer)),
        ("Last Name:", tk.Entry(edit_customer)),
        ("Phone Number:", tk.Entry(edit_customer)),
        ("Email:", tk.Entry(edit_customer))
    ]

    # Create input fields for managing customers
    for label, entry in labels_and_entries:
        tk.Label(
            edit_customer,
            text=label,
            bg=bg_color,
            fg="white",
            font=(font_family, 12)
        ).pack()
        entry.pack()

    # Buttons

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


    add_button.pack()
    edit_button.pack(padx=(10, 10))
    back_button.pack(side = "left", padx=10)
    vehicles_button.pack(side = "left", padx=10)
    services_button.pack(side = "left", padx=10)
    appointments_button.pack(side = "left", padx=10)
    invoices_button.pack(side = "left", padx=10)

    # Refresh the customer list
    refresh_customer_list(customer_listbox)

def load_edit_vehicle():
    edit_vehicle = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_vehicle.grid(row=0, column=0, sticky="nesw")
    edit_vehicle.pack_propagate(False)

    # Create a listbox to display vehicles
    vehicle_listbox = tk.Listbox(edit_vehicle)
    vehicle_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create input fields and buttons for managing vehicles
    enties_and_labels = [
        ("VIN:", tk.Entry(edit_vehicle)),
        ("Customer ID:", tk.Entry(edit_vehicle)),
        ("Make:", tk.Entry(edit_vehicle)),
        ("Model:", tk.Entry(edit_vehicle)),
        ("Year:", tk.Entry(edit_vehicle))
    ]

    entry_values = []

    # Create input fields for managing vehicles
    for label, entry in enties_and_labels:
        tk.Label(
            edit_vehicle,
            text=label,
            bg=bg_color,
            fg="white",
            font=(font_family, 12)
        ).pack()
        entry.pack()
        entry_values.append(entry)

    add_button = tk.Button(
        edit_vehicle,
        text = "Add Vehicle",
        font = ("Calibri", 18),
        fg = "black",
        cursor = "hand2",
        activebackground = button_pressed_color,
        activeforeground="white",
        command=lambda: add_vehicle(
            entry_values[0],
            entry_values[1],
            entry_values[2],
            entry_values[3],
            entry_values[4],
            vehicle_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    edit_button = tk.Button(
        edit_vehicle,
        text="Edit Vehicle",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: modify_vehicle(vehicle_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    button_row = tk.Frame(edit_vehicle, bg=bg_color)
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

    customers_button = tk.Button(
        button_row,
        text="Customers",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: load_edit_customer(),
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

    # Pack the input fields and buttons
    add_button.pack()
    edit_button.pack(padx=(10, 10))
    back_button.pack(side = "left", padx=10)
    customers_button.pack(side = "left", padx=10)
    services_button.pack(side = "left", padx=10)
    appointments_button.pack(side = "left", padx=10)
    invoices_button.pack(side = "left", padx=10)

    # Refresh the vehicle list
    refresh_vehicle_list(vehicle_listbox)

def load_edit_service():
    edit_service = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_service.grid(row=0, column=0, sticky="nesw")
    edit_service.pack_propagate(False)

    # Create a listbox to display services
    service_listbox = tk.Listbox(edit_service)
    service_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create input fields and buttons for managing services
    enties_and_labels = [
        ("Service Name:", tk.Entry(edit_service)),
        ("Description:", tk.Entry(edit_service)),
        ("Price:", tk.Entry(edit_service))
    ]

    entry_values = []

    for label, entry in enties_and_labels:
        tk.Label(
            edit_service,
            text=label,
            bg=bg_color,
            fg="white",
            font=(font_family, 12)
        ).pack()
        entry.pack()
        entry_values.append(entry)

    add_button = tk.Button(
        edit_service,
        text="Add Service",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: add_service(
            service_listbox,
            entry_values[0],
            entry_values[1],
            entry_values[2]),
        relief=tk.FLAT,
        borderwidth=0
    )

    get_description_button = tk.Button(
        edit_service,
        text="Get Description",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: get_description(
            service_listbox
        ),
        relief=tk.FLAT,
        borderwidth=0
    )
        

    edit_button = tk.Button(
        edit_service,
        text="Edit Service",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: modify_service(service_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    delete_button = tk.Button(
        edit_service,
        text="Delete Service",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: delete_service(service_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    button_row = tk.Frame(edit_service, bg=bg_color)
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

    customers_button = tk.Button(
        button_row,
        text="Customers",
        font=("Calibri", 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command = lambda: load_edit_customer(),
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
        activeforeground = "white",
        command=lambda: load_edit_vehicle(),
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
        command=lambda: load_edit_invoice(),
        relief=tk.FLAT,
        borderwidth=0
    )

    # Pack the input fields and buttons
    add_button.pack()
    get_description_button.pack()
    edit_button.pack(padx=(10, 10))
    delete_button.pack(padx=(10, 10))
    back_button.pack(side = "left", padx=10)
    customers_button.pack(side = "left", padx=10)
    vehicles_button.pack(side = "left", padx=10)
    appointments_button.pack(side = "left", padx=10)
    invoices_button.pack(side = "left", padx=10)

    refresh_service_list(service_listbox)

def get_logo(path=r'assets/logo.jpg', resize_factor=0.5):
    try:
        # Create the logo
        original_logo = Image.open(r'assets/logo.jpg')
        width, height = original_logo.size
        new_width = int(width * resize_factor)
        new_height = int(height * resize_factor)

        # Resize the logo
        resized_logo = original_logo.resize((new_width, new_height), Image.LANCZOS)
        return resized_logo
    except FileNotFoundError:
        print(f"Error: logo.jpg not found at: {path}")
        return None

# Create the main window
bg_color = "#08142E"
fg_color = "#FFFFFF"
button_color = "#1b4298"
button_pressed_color = "#becff4"

window_width = 800
window_height = 600

root = tk.Tk()
root.title("Law-Fixit DBMS")
root.geometry(f'{window_width}x{window_height}')
center_window(root, window_width, window_height)
root.eval("tk::PlaceWindow . center")



# Check if the system is macOS
is_macos = root.tk.call('tk', 'windowingsystem') == 'aqua'
# Set the font based on the operating system
if is_macos:
    print("macOS detected")
    font_family = "San Francisco"  # Use Helvetica as a fallback on macOS
else:
    font_family = "Arial"  # Use Arial on other systems

load_main_frame()

# Start the Tkinter main loop
root.mainloop()
