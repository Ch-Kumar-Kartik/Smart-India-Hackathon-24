# Smart-India-Hackathon-24
POV-Our First Attempt at a Hackathon


The Ticket Booking Chatbot is a web-based application designed to assist users in booking tickets for monuments and museums. It provides information on facilities, timings, and directions, and handles ticket bookings with OTP-based mobile number authentication. The chatbot also collects Aadhar numbers during the booking process.

Features
Ticket Booking: Allows users to book tickets for various monuments and museums.
Information Retrieval: Provides answers to basic questions about washroom locations, facilities, timings, and directions.
Authentication: OTP-based login for mobile number verification.
Data Collection: Collects Aadhar numbers during ticket bookings.
Technology Stack
Backend: Python with Flask
Database: MySQL
Frontend: JavaScript, HTML, CSS
Server: Apache
Database Schema
Tables
monuments

ID (INT, AUTO_INCREMENT, PRIMARY KEY): Unique identifier for each monument.
NAME (VARCHAR): Name of the monument.
CITY (VARCHAR): City where the monument is located.
items

id (INT): Foreign key referencing monuments(ID).
product_id (INT, AUTO_INCREMENT, UNIQUE): Unique identifier for ticket types.
ticket_type (ENUM('child', 'adult')): Type of ticket.
price (DECIMAL(4,2)): Price of the ticket.
invoice

ticket_id (INT, PRIMARY KEY, UNIQUE): Unique identifier for each ticket.
id (INT): Foreign key referencing monuments(ID).
product_id (INT): Foreign key referencing items(product_id).
booking_date (DATE): Date of booking.
visit_date (DATE): Date of visit.
no_of_tickets (INT): Number of tickets booked.
phone_number (VARCHAR(10)): Customer’s phone number (must be 10 digits).
email (VARCHAR(255)): Customer’s email address.
aadhar_id (CHAR(12)): Customer’s Aadhar number.
