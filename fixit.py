import sqlite3
import tkinter as tk
from tkinter import messagebox, Spinbox, ttk
from tkcalendar import Calendar
from PIL import ImageTk, Image
from customer_functions import *
from vehicle_functions import *
from service_functions import *
from appointment_functions import *
from invoice_functions import *
from time_utils import *

# Initialize the SQLite database
connection = sqlite3.connect('mechanic_shop.db')
cursor = connection.cursor()

def get_vehicles_for_customer(customer_id_entry, vehicle_var, vehicle_combobox):
    customer_id = customer_id_entry.get()
    try:
        cursor.execute('''
            SELECT VIN, year, make, model FROM Vehicles WHERE customer_id = ?
        ''', (customer_id,))
        vehicles = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e)
        return
    # Clear Values in Combobox
    vehicle_combobox.set("")
    vehicle_combobox['values'] = []
    if not vehicles:
        messagebox.showerror("Error", "No vehicles found for this customer.")
    else:
        # Extract VINs from the result and create a list of strings for the combobox
        display_values = [f"{year} {make} {model}" for _, year, make, model in vehicles]

        # Set the values of the combobox
        vehicle_combobox['values'] = display_values

        # Function to set the selected VIN in the variable
        def set_vehicle_var(event):
            index = vehicle_combobox.current()
            if index >= 0:
                vehicle_var.set(vehicles[index][0])
        
        # Bind the event handler to the <<ComboboxSelected>> event
        vehicle_combobox.bind("<<ComboboxSelected>>", set_vehicle_var)
def get_services():
    cursor.execute('''
        SELECT service_id, service_name FROM Services
    ''')
    services = cursor.fetchall()
    return services

def get_appointments():
    cursor.execute('''
        SELECT appointment_id FROM Appointments
    ''')
    appointments = cursor.fetchall()
    return appointments

def get_vehicles():
    cursor.execute('''
        SELECT VIN, make, model FROM Vehicles
    ''')
    vehicles = cursor.fetchall()
    return vehicles

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

    for frame in frames:
        frame.destroy()

    frames.append(welcome_frame)

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

    for frame in frames:
        frame.destroy()

    frames.append(edit_customer)

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

    entry_values = []

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
        entry_values.append(entry)

    # Buttons

    add_button = tk.Button(
        edit_customer, 
        text="Add Customer",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        activeforeground="white",
        command=lambda: add_customer(
            entry_values[0],
            entry_values[1],
            entry_values[2],
            entry_values[3],
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
    
    frames.append(button_row)

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

    for frame in frames:
        frame.destroy()

    frames.append(edit_vehicle)

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

    frames.append(button_row)

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

    for frame in frames:
        frame.destroy()

    frames.append(edit_service)

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

    frames.append(button_row)

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

def load_edit_appointment():
    # Create the main frame
    edit_appointment = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_appointment.grid(row=0, column=0, columnspan=2, rowspan = 4, sticky="nesw")
    edit_appointment.pack_propagate(False)

    frames.append(edit_appointment)

    # Create a listbox to display appointments
    appointment_listbox = tk.Listbox(edit_appointment)
    appointment_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    refresh_invoice_list(appointment_listbox)

    # Create the left and right frames
    left_frame = tk.Frame(edit_appointment, bg = bg_color)
    left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    left_frame.place(relx=1/5, rely=0.55, anchor="center")

    frames.append(left_frame)

    right_frame = tk.Frame(edit_appointment, bg=bg_color)
    right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")
    right_frame.place(relx=2/3, rely=0.5, anchor="center")

    frames.append(right_frame)

    # Create the time frame with the right frame
    time_frame = tk.Frame(right_frame, bg=bg_color)
    time_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    time_frame.place(relx=3/4, rely=1/3, anchor="center")

    frames.append(time_frame)

    date_entry = tk.Entry(right_frame)
    date_entry.grid(row = 0, column = 0, padx = 10, sticky="ew")

    time_label = tk.Label(right_frame, text="Appointment Time: \n Reminder that we accept appointments \n between 8:00 and 17:00", bg=bg_color, fg="white", font=(font_family, 12))
    time_label.grid(row = 0, column = 1, padx = 5, sticky="w")

    hour_spinbox = Spinbox(time_frame, from_=8, to = 17, width = 2)
    hour_spinbox.grid(row = 0, column = 1, pady=5)
    colon_label = tk.Label(time_frame, text=":", bg=bg_color, fg="white", font=(font_family, 12))
    colon_label.grid(row = 0, column = 2, pady=5)
    minute_spinbox = Spinbox(time_frame, from_=0, to = 59, width = 2)
    minute_spinbox.grid(row = 0, column = 3, pady=5)

    calendar = Calendar(right_frame, selectmode="day")
    calendar.grid(row = 1, column = 0, padx = 10, sticky="nsw")

    select_date_button = tk.Button(right_frame, text="Select Date",font = (font_family, 12), bg=bg_color, command = lambda: get_selected_date(calendar, date_entry, hour_spinbox, minute_spinbox, True))
    select_date_button.grid(row = 2, column = 0, padx = 10, sticky="ew")

    customer_id_label = tk.Label(
        left_frame,
        text="Customer ID:",
        bg=bg_color,
        fg="white",
        font=(font_family, 12)
    )
    customer_id_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
    customer_id_entry = tk.Entry(left_frame)
    customer_id_entry.grid(row=1, column=0, sticky="w", padx=(0, 10))
    service_label = tk.Label(
        left_frame,
        text="Service Name:",
        bg=bg_color,
        fg="white",
        font=(font_family, 12)
    )
    service_label.grid(row=2, column=0, sticky="w", padx=(0, 10))

    services = get_services()
    selected_service = tk.StringVar()

    # Use the display names for the combobox values
    service_combobox = ttk.Combobox(left_frame, textvariable=selected_service, values=services, state="readonly")
    service_combobox.grid(row=3, column=0, sticky="w", padx=(0, 10))


    vehicle_label = tk.Label(left_frame, text="Vehicle ID:", bg=bg_color, fg="white", font=(font_family, 12))
    vehicle_label.grid(row=4, column=0, sticky="w", padx=(0, 10))

    vehicle_var = tk.StringVar()

    vehicle_combobox = ttk.Combobox(left_frame, textvariable=vehicle_var, state="readonly")
    vehicle_combobox.grid(row=5, column=0, sticky="w", padx=(0, 10))

    update_vehicle_button = tk.Button(
        left_frame,
        text="Update Vehicle List",
        font = (font_family, 12),
        bg=bg_color,
        command = lambda: get_vehicles_for_customer(customer_id_entry, vehicle_var, vehicle_combobox),
        cursor = "hand2",
        relief=tk.FLAT,
        borderwidth=0
    )
    update_vehicle_button.grid(row=6, column=0, sticky="w", pady = 5)
    
    # Drop-down menu for status
    selected_status = tk.StringVar()
    status_options = [
        "Pending",
        "In Progress",
        "Completed"
    ]
    status_label = tk.Label(left_frame, text="Status:", bg=bg_color, fg="white", font=(font_family, 12))
    status_label.grid(row=7, column=0, sticky="w", pady=5)
    status_dropdown = ttk.Combobox(left_frame, textvariable=selected_status, values=status_options, state="readonly")
    selected_status.set(status_options[0])
    status_dropdown.grid(row=8, column=0, pady=5, sticky="w")

    button_column = tk.Frame(edit_appointment, bg=bg_color)
    button_column.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
    button_column.place(relx = 0.5, rely = 0.8, anchor="center")

    frames.append(button_column)

    add_button = tk.Button(
        button_column,
        text="Add Appointment",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: add_appointment(
            appointment_listbox,
            customer_id_entry,
            vehicle_var,
            selected_service,
            date_entry,
            selected_status,
            ),
        relief=tk.FLAT,
        borderwidth=0
    )

    edit_button = tk.Button(
        button_column,
        text="Edit Appointment",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: modify_appointment(appointment_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    delete_button = tk.Button(
        button_column,
        text="Delete Appointment",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: delete_appointment(appointment_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    button_row = tk.Frame(edit_appointment, bg=bg_color)
    button_row.grid(row=3, column=0, columnspan=2, sticky="s")
    button_row.pack(side=tk.BOTTOM)
    
    frames.append(button_row)

    back_button = tk.Button(
        button_row,
        text="Back",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_main_frame(),
        relief=tk.FLAT,
        borderwidth=0
    )

    customers_button = tk.Button(
        button_row,
        text="Customers",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_customer(),
        relief=tk.FLAT,
        borderwidth=0
    )
    
    vehicles_button = tk.Button(
        button_row,
        text="Vehicles",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_vehicle(),
        relief=tk.FLAT,
        borderwidth=0
    )

    services_button = tk.Button(
        button_row,
        text="Services",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_service(),
        relief=tk.FLAT,
        borderwidth=0
    )

    invoices_button = tk.Button(
        button_row,
        text="Invoices",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_invoice(),
        relief=tk.FLAT,
        borderwidth=0
    )

    add_button.grid(row = 0, column = 0, padx=(10, 0), sticky="ew")
    edit_button.grid(row = 1, column = 0, padx=(10, 0), sticky="ew")
    delete_button.grid(row = 2, column = 0, padx=(10, 0), sticky="ew")
    back_button.pack(side = "left", padx=10)
    customers_button.pack(side = "left", padx=10)
    vehicles_button.pack(side = "left", padx=10)
    services_button.pack(side = "left", padx=10)
    invoices_button.pack(side = "left", padx=10)


    edit_appointment.grid_columnconfigure(0, weight=1)
    edit_appointment.grid_columnconfigure(1, weight=1)

    button_column.grid_columnconfigure(1, weight=1)
    button_column.grid_rowconfigure(0, weight=1)

    # Refresh the appointment list
    refresh_appointment_list(appointment_listbox)

def load_edit_invoice():
    # Create the main frame
    edit_invoice = tk.Frame(root, width=window_width, height=window_height, bg=bg_color)
    edit_invoice.grid(row=0, column=0, sticky="nesw")
    edit_invoice.pack_propagate(False)

    frames.append(edit_invoice)

    # Create a listbox to display invoices
    invoice_listbox = tk.Listbox(edit_invoice)
    invoice_listbox.pack(fill=tk.BOTH, padx=10, pady=10)


    edit_button = tk.Button(
        edit_invoice,
        text="Edit Invoice",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: modify_invoice(invoice_listbox),
        relief=tk.FLAT,
        borderwidth=0
    )

    button_row = tk.Frame(edit_invoice, bg=bg_color)
    button_row.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="sew")
    button_row.pack(side=tk.BOTTOM)

    frames.append(button_row)

    back_button = tk.Button(
        button_row,
        text="Back",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_main_frame(),
        relief=tk.FLAT,
        borderwidth=0
    )

    customers_button = tk.Button(
        button_row,
        text="Customers",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_customer(),
        relief=tk.FLAT,
        borderwidth=0
    )

    vehicles_button = tk.Button(
        button_row,
        text="Vehicles",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_vehicle(),
        relief=tk.FLAT,
        borderwidth=0
    )

    services_button = tk.Button(
        button_row,
        text="Services",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_service(),
        relief=tk.FLAT,
        borderwidth=0
    )

    appointments_button = tk.Button(
        button_row,
        text="Appointments",
        font=(font_family, 18),
        fg="black",
        cursor="hand2",
        activebackground=button_pressed_color,
        command=lambda: load_edit_appointment(),
        relief=tk.FLAT,
        borderwidth=0
    )

    

    # Pack buttons
    edit_button.pack()
    back_button.pack(side = "left", padx=10)
    customers_button.pack(side = "left", padx=10)
    vehicles_button.pack(side = "left", padx=10)
    services_button.pack(side = "left", padx=10)
    appointments_button.pack(side = "left", padx=10)

    edit_invoice.grid_columnconfigure(0, weight=1)
    edit_invoice.grid_columnconfigure(1, weight=1)

    refresh_invoice_list(invoice_listbox)


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

frames = []

# Check if the system is macOS
is_macos = root.tk.call('tk', 'windowingsystem') == 'aqua'
# Set the font based on the operating system
if is_macos:
    font_family = "San Francisco"  # Use Helvetica as a fallback on macOS
else:
    font_family = "Arial"  # Use Arial on other systems

load_main_frame()

# Start the Tkinter main loop
root.mainloop()
