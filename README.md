# Law-Fixit
This is my final project for CS 348, a database management app that manages a database for a car mechanic shop

## Database Design
`Customers (customer_id, first_name, last_name, phone_number, email_address)`
-	Stores information about the customers that visit the shop.
-	I will not add delete functionality since we want to keep all customers for the records, even if they never return.
-	I will add editing functionality since it is possible for a customer to change all of their attributes, except ID.
-	Each customer is given a unique ID, which is incremented for each customer added to the DB. For example, the 5th customer is assigned 5, the 6th assigned 6…

`Vehicles (VIN, customer_id, make, model, year)`
-	Stores information about the vehicles that are serviced in the shop.
-	I will use the car’s VIN as the primary key since it is unique between vehicles.
-	customer_id is the foreign key that links a vehicle to the customer that brought it in.
-	I will not add delete functionality to this table since I want to keep the data for records.
-	I will add edit functionality for the customer_id since cars can be sold to new customers.

`Services (service_id, service_name, description, price)`
-	Lists services that the store will provide.
-	I will add edit and delete functionalities to allow the store to change the services it provides as it evolves.
-	Each service has a service_id.

`Appointments (appointment_id, customer_id, vehicle_id, service_id, appointment_date, status)`
-	Tracks service appointments.
-	Links to customers, vehicles, and services through customer_id, vehicle_id, and service_id foreign keys respectively.
-	Will have edit and delete functionalities to handle cases where a customer wants to change the services they get, change what vehicle they get serviced, or cancel their appointment. appointment_id cannot be edited.

`Invoices (invoice_id, appointment_id, total_amount, payment_status, invoice_date)`
-	Holds records for previous appointments.
-	Will add edit functionalities for payment_status so it can be updated when the customer pays.
-	Cannot be deleted as the store wants to keep these in their records, even if a customer never returns.

## System Requirements
Python installation with Tkinter installed.
Currrently tested on Anaconda Python 3.15 and Tkinter 8.6
