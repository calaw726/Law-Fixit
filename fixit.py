import sqlite3
import os
import tkinter as tk
from tkinter import messagebox, Spinbox, ttk
from tkcalendar import Calendar
from PIL import ImageTk, Image

# Background and foreground colors
BG_COLOR = "#08142E"
FG_COLOR = "#FFFFFF"
BT_COLOR = "#1b4298"
BT_P_COLOR = "#becff4"

# Window dimensions
WIN_W = 1000
WIN_H = 750


from customer_functions import *
from vehicle_functions import *
from service_functions import *
from appointment_functions import *
from invoice_functions import *
from time_utils import *

# Initialize the SQLite database
connection = sqlite3.connect('mechanic_shop.db')
cursor = connection.cursor()



def create_button(parent, text, command, **kwargs):
    # Define Button Style
    BUTTON_STYLE = {
        "font": (font_family, 18),
        "cursor": "hand2",
        "activebackground": BT_P_COLOR,
        "borderwidth": 0,
        "relief": tk.FLAT,
        **kwargs
    }
    return tk.Button(parent, text=text, command=command, **BUTTON_STYLE)

def create_labeled_entry(parent, label_text):
    label = tk.Label(parent, text=label_text, bg=BG_COLOR, fg=FG_COLOR, font=(font_family, 12))
    entry = tk.Entry(parent)
    label.pack(pady=(5, 0))
    entry.pack(pady=(0, 5))
    return entry

def create_labeled_combobox(parent, text=None, **kwargs):
    if text:
        label = tk.Label(parent, text=text, bg=BG_COLOR, fg=FG_COLOR, font=(font_family, 12))
        label.pack(pady=(5, 0))
    combobox = ttk.Combobox(parent, **kwargs)
    combobox.pack(pady=5)
    return combobox

def create_navigation_button(parent, text, command):
    return create_button(parent, text, command, padx=10)

def get_vehicles_for_customer(customer_id_entry, vehicle_var, vehicle_combobox):
    customer_id = customer_id_entry.get()
    if not(customer_id and customer_id[0].isdigit()):
        messagebox.showerror("Error", "Please select a customer in the dropdown menu above.")
        return
    
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

def get_customers_with_vehicles(customer_var, customer_combobox):
    try:
        # Fetch customers with vehicles
        cursor.execute('''
            SELECT * FROM customers_with_vehicles;
        ''')
        customers = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e)
        return
    
    # Clear Values in Combobox
    customer_combobox.set("")
    customer_combobox['values'] = []

    if not customers:
        messagebox.showerror("Error", "No customers found.")
    else:
        # Extract customer IDs from the result and create a list of strings for the combobox
        display_values = [f"{id}: {first_name} {last_name}" for id, first_name, last_name in customers]

        # Set the values of the combobox
        customer_combobox['values'] = display_values

        # Function to set the selected customer_id in the variable
        def set_customer_var(event):
            index = customer_combobox.current()
            if index >= 0:
                customer_var.set(customers[index][0])
        
        # Bind the event handler to the <<ComboboxSelected>> event
        customer_combobox.bind("<<ComboboxSelected>>", set_customer_var)

def center_window(window, width=None, height=None):
    req_width = window.winfo_reqwidth() if width is None else width
    req_height = window.winfo_reqheight() if height is None else height

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - req_width) // 2
    y = (screen_height - req_height) // 2

    window.geometry(f'{req_width}x{req_height}+{x}+{y}')

def load_main_frame():
    # Create the main frame
    welcome_frame = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    welcome_frame.grid(row=0, column=0, sticky="nesw")
    welcome_frame.pack_propagate(False)

    # Destroy previous frames
    for frame in frames:
        frame.destroy()

    frames.append(welcome_frame)

    # Create the logo
    logo_img = ImageTk.PhotoImage(get_logo("assets/logo.ico", 2))
    logo_widget = tk.Label(welcome_frame, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack(fill=tk.BOTH, pady=10)

    # Create the buttons
    get_upcoming_appointments_button = create_button(welcome_frame, "Upcoming Appointments", lambda: load_upcoming_appointments()).pack(pady=5)
    process_transaction_button = create_button(welcome_frame, "Process Transaction", lambda: load_edit_invoice()).pack(pady=5)
    edit_tables_button = create_button(welcome_frame, "Edit Tables", lambda: load_edit_customer()).pack(pady=5)

    center_window(root, WIN_W, WIN_H)

def load_edit_customer():
    edit_customer = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
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
        ("First Name:", create_labeled_entry(edit_customer, "First Name:")),
        ("Last Name:", create_labeled_entry(edit_customer, "Last Name:")),
        ("Phone Number:", create_labeled_entry(edit_customer, "Phone Number:")),
        ("Email:", create_labeled_entry(edit_customer, "Email:"))
    ]

    entry_values = [entry for _, entry in labels_and_entries]

    # Buttons
    add_button = create_button(edit_customer, "Add Customer", lambda: add_customer(*entry_values, customer_listbox))
    edit_button = create_button(edit_customer, "Edit Customer", lambda: modify_customer(customer_listbox))

    button_row =tk.Frame(edit_customer, bg=BG_COLOR)
    button_row.grid(row=1, column=0, sticky="nesw")
    button_row.pack(side=tk.BOTTOM)
    frames.append(button_row)

    # Navigation buttons
    back_button = create_navigation_button(button_row, "Back", lambda: load_main_frame())
    vehicles_button = create_navigation_button(button_row, "Vehicles", lambda: load_edit_vehicle())
    services_button = create_navigation_button(button_row, "Services", lambda: load_edit_service())
    appointments_button = create_navigation_button(button_row, "Appointments", lambda: load_edit_appointment())
    invoices_button = create_navigation_button(button_row, "Invoices", lambda: load_edit_invoice())

    # Pack Buttons
    for button in [add_button, edit_button]:
        button.pack(pady=5)

    # Pack Nav buttons
    for button in [back_button, vehicles_button, services_button, appointments_button, invoices_button]:
        button.pack(side="left", padx=10, pady=5)

    # Refresh the customer list
    refresh_customer_list(customer_listbox)

def load_edit_vehicle():
    edit_vehicle = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    edit_vehicle.grid(row=0, column=0, sticky="nesw")
    edit_vehicle.pack_propagate(False)

    for frame in frames:
        frame.destroy()

    frames.append(edit_vehicle)

    # Create a listbox to display vehicles
    vehicle_listbox = tk.Listbox(edit_vehicle)
    vehicle_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create input fields and buttons for managing vehicles
    entries_and_labels = [
        ("VIN:", create_labeled_entry(edit_vehicle, "VIN:")),
        ("Customer ID:", create_labeled_combobox(edit_vehicle, text="Customer ID", state="readonly")),
        ("Make:", create_labeled_entry(edit_vehicle, "Make:")),
        ("Model:", create_labeled_entry(edit_vehicle, "Model:")),
        ("Year:", create_labeled_entry(edit_vehicle, "Year:"))
    ]

    entry_values = [entry for _, entry in entries_and_labels]

    list_customers(entry_values[1], entries_and_labels[1][1])

    add_button = create_button(edit_vehicle, "Add Vehicle", lambda: add_vehicle(*entry_values, vehicle_listbox))
    edit_button = create_button(edit_vehicle, "Edit Vehicle", lambda: modify_vehicle(vehicle_listbox))

    button_row = tk.Frame(edit_vehicle, bg=BG_COLOR)
    button_row.grid(row=1, column=0, sticky="nesw")
    button_row.pack(side=tk.BOTTOM)

    frames.append(button_row)
    navigation_buttons = [
        create_navigation_button(button_row, "Back", lambda: load_main_frame()),
        create_navigation_button(button_row, "Customers", lambda: load_edit_customer()),
        create_navigation_button(button_row, "Services", lambda: load_edit_service()),
        create_navigation_button(button_row, "Appointments", lambda: load_edit_appointment()),
        create_navigation_button(button_row, "Invoices", lambda: load_edit_invoice())
    ]

    # Pack the input fields and buttons
    for button in [add_button, edit_button]:
        button.pack(pady=5)
    
    for button in navigation_buttons:
        button.pack(side="left", padx=10, pady=5)

    # Refresh the vehicle list
    refresh_vehicle_list(vehicle_listbox)

def load_edit_service():
    edit_service = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    edit_service.grid(row=0, column=0, sticky="nesw")
    edit_service.pack_propagate(False)

    for frame in frames:
        frame.destroy()

    frames.append(edit_service)

    # Create a listbox to display services
    service_listbox = tk.Listbox(edit_service)
    service_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create input fields and buttons for managing services
    entries_and_labels = [
        ("Service Name:", create_labeled_entry(edit_service, "Service Name:")),
        ("Description:", create_labeled_entry(edit_service, "Description:")),
        ("Price:", create_labeled_entry(edit_service, "Price:"))
    ]

    entry_values = [entry for _, entry in entries_and_labels]

    add_button = create_button(edit_service, "Add Service", lambda: add_service(service_listbox, *entry_values))
    get_description_button = create_button(edit_service, "Get Description", lambda: get_description(service_listbox))
    edit_button = create_button(edit_service, "Edit Service", lambda: modify_service(service_listbox))
    delete_button = create_button(edit_service, "Delete Service", lambda: delete_service(service_listbox))

    button_row = tk.Frame(edit_service, bg=BG_COLOR)
    button_row.grid(row=1, column=0, sticky="nesw")
    button_row.pack(side=tk.BOTTOM)

    frames.append(button_row)

    navigation_buttons = [
        create_navigation_button(button_row, "Back", lambda: load_main_frame()),
        create_navigation_button(button_row, "Customers", lambda: load_edit_customer()),
        create_navigation_button(button_row, "Vehicles", lambda: load_edit_vehicle()),
        create_navigation_button(button_row, "Appointments", lambda: load_edit_appointment()),
        create_navigation_button(button_row, "Invoices", lambda: load_edit_invoice())
    ]

    # Pack the input fields and buttons
    for button in (add_button, get_description_button, edit_button, delete_button):
        button.pack(pady=5)
    
    for button in navigation_buttons:
        button.pack(side="left", padx=10, pady=5)

    refresh_service_list(service_listbox)

def load_edit_appointment():
    # Create the main frame
    edit_appointment = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    edit_appointment.grid(row=0, column=0, columnspan=2, rowspan = 4, sticky="nesw")
    edit_appointment.pack_propagate(False)

    frames.append(edit_appointment)

    # Create a listbox to display appointments
    appointment_listbox = tk.Listbox(edit_appointment)
    appointment_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    refresh_appointment_list(appointment_listbox)

    # Create the left and right frames
    left_frame = tk.Frame(edit_appointment, bg = BG_COLOR)
    left_frame.place(relx=1/5, rely=0.55, anchor="center")

    frames.append(left_frame)

    right_frame = tk.Frame(edit_appointment, bg=BG_COLOR)
    right_frame.place(relx=2/3, rely=0.5, anchor="center")

    frames.append(right_frame)

    # Create the time frame with the right frame
    time_frame = tk.Frame(right_frame, bg=BG_COLOR)
    time_frame.place(relx=3/4, rely=1/3, anchor="center")

    frames.append(time_frame)
    date_var = tk.StringVar()
    date_entry = tk.Entry(right_frame, textvariable=date_var, state="readonly")
    date_entry.grid(row = 0, column = 0, sticky="ew")

    time_label = tk.Label(right_frame, text="Appointment Time: \n Reminder that we accept appointments \n between 8:00 and 17:00", bg=BG_COLOR, fg=FG_COLOR, font=(font_family, 12))
    time_label.grid(row = 0, column = 1, sticky="ew", pady=5)

    hour_spinbox = Spinbox(time_frame, from_=8, to = 16, width = 2)
    hour_spinbox.grid(row = 0, column = 1, pady=5, sticky="ew")
    colon_label = tk.Label(time_frame, text=":", bg=BG_COLOR, fg="white", font=(font_family, 12))
    colon_label.grid(row = 0, column = 2, pady=5, sticky="ew")
    minute_spinbox = Spinbox(time_frame, from_=0, to = 59, width = 2)
    minute_spinbox.grid(row = 0, column = 3, pady=5, sticky="ew")

    calendar = Calendar(right_frame, selectmode="day")
    calendar.grid(row = 1, column = 0, padx = 10, sticky="nsw")

    select_date_button = tk.Button(
        right_frame,
        text="Select Date", 
        font = (font_family, 12),
        command = lambda: get_selected_date(
            calendar,
            date_var,
            hour_spinbox,
            minute_spinbox,
            True
        )
        )
    select_date_button.grid(row = 2, column = 0, sticky="ew")

    customer_id_label = tk.Label(
        left_frame,
        text="Customer ID:",
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=(font_family, 12)
    )
    customer_id_label.grid(row=0, column=0, sticky="ew", pady=5)
    customer_var = tk.StringVar()
    customer_combobox = ttk.Combobox(left_frame, textvariable=customer_var, state="readonly")
    customer_combobox.grid(row=1, column=0, sticky="ew", pady=5)
    get_customers_with_vehicles(customer_var, customer_combobox)

    service_label = tk.Label(
        left_frame,
        text="Service Name:",
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=(font_family, 12)
    )
    service_label.grid(row=2, column=0, sticky="ew", pady=5)

    services = get_services()
    selected_service = tk.StringVar()

    # Use the display names for the combobox values
    service_combobox = ttk.Combobox(left_frame, textvariable=selected_service, values=services, state="readonly")
    service_combobox.grid(row=3, column=0, sticky="ew", pady=5)

    vehicle_label = tk.Label(left_frame, text="Vehicle ID:", bg=BG_COLOR, fg="white", font=(font_family, 12))
    vehicle_label.grid(row=4, column=0, sticky="ew", pady=5)

    vehicle_var = tk.StringVar()

    vehicle_combobox = ttk.Combobox(left_frame, textvariable=vehicle_var, state="readonly")
    vehicle_combobox.grid(row=5, column=0, sticky="ew", pady=5)

    update_vehicle_button = tk.Button(
        left_frame,
        text="Update Vehicle List",
        font = (font_family, 12),
        activebackground=BT_P_COLOR,
        command = lambda: get_vehicles_for_customer(customer_var, vehicle_var, vehicle_combobox),
        cursor = "hand2",
        relief=tk.FLAT,
        borderwidth=0
    )
    update_vehicle_button.grid(row=6, column=0, sticky="ew", pady = (10, 5))
    
    # Drop-down menu for status
    selected_status = tk.StringVar()
    status_options = [
        "Pending",
        "In Progress",
        "Completed"
    ]
    status_label = tk.Label(left_frame, text="Status:", bg=BG_COLOR, fg="white", font=(font_family, 12))
    status_label.grid(row=7, column=0, sticky="ew", pady=5)
    status_dropdown = ttk.Combobox(left_frame, textvariable=selected_status, values=status_options, state="readonly")
    selected_status.set(status_options[0])
    status_dropdown.grid(row=8, column=0, pady=5, sticky="ew")

    button_column = tk.Frame(edit_appointment, bg=BG_COLOR)
    button_column.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
    button_column.place(relx = 0.5, rely = 0.8, anchor="center",)

    frames.append(button_column)

    add_button = create_button(button_column, "Add Appointment", lambda: add_appointment(appointment_listbox, customer_var, vehicle_var, selected_service, date_entry, selected_status))
    edit_button = create_button(button_column, "Edit Appointment", lambda: modify_appointment(appointment_listbox))
    delete_button = create_button(button_column, "Delete Appointment", lambda: delete_appointment(appointment_listbox))

    button_row = tk.Frame(edit_appointment, bg=BG_COLOR)
    button_row.pack(side=tk.BOTTOM)
    
    frames.append(button_row)

    navigation_buttons = [
        create_navigation_button(button_row, "Back", lambda: load_main_frame()),
        create_navigation_button(button_row, "Customers", lambda: load_edit_customer()),
        create_navigation_button(button_row, "Vehicles", lambda: load_edit_vehicle()),
        create_navigation_button(button_row, "Services", lambda: load_edit_service()),
        create_navigation_button(button_row, "Invoices", lambda: load_edit_invoice())
    ]

    for button in [add_button, edit_button, delete_button]:
        button.pack(pady=5, fill=tk.X)

    for button in navigation_buttons:
        button.pack(side="left", padx=10, pady=5)

    edit_appointment.grid_columnconfigure(0, weight=1)
    edit_appointment.grid_columnconfigure(1, weight=1)

    button_column.grid_columnconfigure(1, weight=1)
    button_column.grid_rowconfigure(0, weight=1)

def load_edit_invoice():
    # Create the main frame
    edit_invoice = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    edit_invoice.grid(row=0, column=0, sticky="nesw")
    edit_invoice.pack_propagate(False)
    frames.append(edit_invoice)

    # Create a listbox to display invoices
    invoice_listbox = tk.Listbox(edit_invoice)
    invoice_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    edit_button = create_button(edit_invoice, "Process Transaction", lambda: modify_invoice(invoice_listbox))

    button_row = tk.Frame(edit_invoice, bg=BG_COLOR)
    button_row.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="sew")
    button_row.pack(side=tk.BOTTOM)
    frames.append(button_row)

    navigation_buttons = [
        create_navigation_button(button_row, "Back", lambda: load_main_frame()),
        create_navigation_button(button_row, "Customers", lambda: load_edit_customer()),
        create_navigation_button(button_row, "Vehicles", lambda: load_edit_vehicle()),
        create_navigation_button(button_row, "Services", lambda: load_edit_service()),
        create_navigation_button(button_row, "Appointments", lambda: load_edit_appointment())
    ]

    # Pack buttons
    edit_button.pack()
    for button in navigation_buttons:
        button.pack(side="left", padx=10, pady=5)

    edit_invoice.grid_columnconfigure(0, weight=1)
    edit_invoice.grid_columnconfigure(1, weight=1)

    refresh_invoice_list(invoice_listbox)

def load_upcoming_appointments():
    upcoming_appointments_frame = tk.Frame(root, width=WIN_W, height=WIN_H, bg=BG_COLOR)
    upcoming_appointments_frame.grid(row=0, column=0, sticky="nesw")
    upcoming_appointments_frame.pack_propagate(False)

    for frame in frames:
        frame.destroy()
    
    frames.append(upcoming_appointments_frame)

    # Create a listbox to display upcoming appointments
    upcoming_appointments_listbox = tk.Listbox(upcoming_appointments_frame, height=WIN_H // 20)
    upcoming_appointments_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

    get_upcomming_appointments(upcoming_appointments_listbox)

    button_row = tk.Frame(upcoming_appointments_frame, bg=BG_COLOR)
    button_row.grid(row=1, column=0, sticky="nesw")
    button_row.pack(side=tk.BOTTOM)

    back_button = create_navigation_button(button_row, "Back", lambda: load_main_frame())
    back_button.pack(pady=5)

    upcoming_appointments_frame.grid_rowconfigure(0, weight=3)
    button_row.grid_rowconfigure(0, weight=1)

def get_logo(path=None, resize_factor=0.5):
    if path is None:
        path = os.path.join('assets', 'logo.jpg')

    try:
        # Create the logo
        original_logo = Image.open(path)
        width, height = original_logo.size
        new_width = int(width * resize_factor)
        new_height = int(height * resize_factor)

        # Resize the logo
        resized_logo = original_logo.resize((new_width, new_height), Image.LANCZOS)
        return resized_logo
    except FileNotFoundError:
        print(f"Error: logo.jpg not found at: {path}")
        return None

root = tk.Tk()
root.title("Law-Fixit DBMS")

# Set the window size and position
root.geometry(f'{WIN_W}x{WIN_H}')
center_window(root, WIN_W, WIN_H)

# Disable resizing
root.resizable(False, False)

frames = []

# Check if the system is macOS
is_macos = root.tk.call('tk', 'windowingsystem') == 'aqua'

# Set the font based on the operating system
font_family = "San Francisco" if is_macos else "Verdana"

# Set the icon
if is_macos:
    logo = ImageTk.PhotoImage(get_logo("assets/logo.ico"))
    root.iconphoto(True, logo)
else:
    root.iconbitmap(default="assets/logo.ico")

# Set the background color
root.configure(bg=BG_COLOR)

load_main_frame()

# Start the Tkinter main loop
root.mainloop()