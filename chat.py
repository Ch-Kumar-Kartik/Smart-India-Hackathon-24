import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import smtplib
import qrcode
from PIL import Image
import pymysql

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Use raw string to handle special characters in the file path
with open(r"C:/Users/kanak/Downloads/SIH24/intents.json", 'r') as json_data:
    intents = json.load(json_data)

FILE = r"C:/Users/kanak/Downloads/SIH24/data.pth"
data = torch.load(FILE, weights_only=True)  # Set weights_only=True

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

# Replace these with your actual database credentials
host = 'localhost'
user = 'root'
password = 'kanak1234'
database = 'SIH'

# Establish the connection
db = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = db.cursor()

# Variables to store user inputs
user_data = {}

def generate_qr_code(data, filename="qr_code.png"):
    """Generate a QR code image from the given data and display it."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    img.show()  # Display the QR code image
    return filename

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # Menu options: booking, information, or retrieving ticket
                if tag == "menu":
                    return "Please select an option:\n1. Book a Ticket\n2. Get Information\n3. Retrieve Booking"

                # Capture user data based on the conversation flow
                # Initialize user_data
                user_data = {}
                otp_verified = False

                if tag == "museum_name":
                    museum_name = msg.strip()
                    user_data["museum_name"] = museum_name
                    print(f"Querying for museum_name: {museum_name}")  # Debugging line
                    cursor.execute("SELECT ID FROM monuments WHERE NAME = %s", (museum_name,))
                    result = cursor.fetchone()
                    if result:
                        print(f"Found result: {result}")  # Debugging line
                        user_data["product_id"] = result[0]
                        return "Got it! Now, please provide the visit date in YYYY-MM-DD."
                    else:
                        print("Museum not found.")  # Debugging line
                        return "Sorry, I couldn't find that museum. Could you please provide a valid museum name?"

                elif tag == "visit_date":
                    visit_date = msg.strip()  # Define visit_date
                    user_data["visit_date"] = visit_date
                    print(f"Received visit date: {visit_date}")  # Debugging line
                    return "Thank you. How many adults will be visiting?"

                elif tag == "number_of_adults":
                    user_data["adults"] = int([int(s) for s in msg.split() if s.isdigit()][0])
                    return "Thank you. How many children will be visiting?"

                elif tag == "number_of_children":
                    user_data["children"] = int([int(s) for s in msg.split() if s.isdigit()][0])
                    
                    product_id = user_data.get("product_id")
                    if product_id:

                            # Fetch adult and child ticket prices
                            cursor.execute("SELECT price FROM items WHERE product_id = %s AND ticket_type = 'adult'", (product_id,))
                            adult_price = cursor.fetchone()
                            cursor.execute("SELECT price FROM items WHERE product_id = %s AND ticket_type = 'child'", (product_id,))
                            child_price = cursor.fetchone()

                            # Check if prices are found
                            if adult_price and child_price:
                                # Calculate total cost
                                total_cost = (user_data["adults"] * adult_price[0]) + (user_data["children"] * child_price[0])
                                user_data["total_cost"] = total_cost
                                return f"Great! The total cost for {user_data['adults']} adults and {user_data['children']} children is ${total_cost:.2f}. Please provide your name."
    
                elif tag == "name":
                    user_data["name"] = msg.split("name is")[-1].strip()
                    return f"Got it, {user_data['name']}. Could you share your mobile number?"

                elif tag == "mobile_number":
                    user_data["mobile_number"] = msg.split("mobile number is")[-1].strip()
                    return "Thank you for sharing your mobile number. May I have your email address?"

                elif tag == "email":
                    user_data["email"] = msg.split("email is")[-1].strip()
                    otp_verified = False
                    # Generating a random 6-digit number as OTP
                    OTP = random.randint(100000, 999999)

                    # SMTP server configuration
                    smtp_server = "smtp.mailersend.net"
                    smtp_port = 587  # SSL port

                    # Sender email and password
                    sender_email = "MS_zofGYv@trial-z3m5jgrrwkogdpyo.mlsender.net"
                    password = "6dQF6CiWGvIkG8KH"  # Update with your Rediffmail password

                    try:
                        # Setting up the server with SSL
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()
                            server.login(sender_email, password)  # Logging into the sender's email account

                            
                            receiver_email = user_data["email"]

                            def email_verification(receiver_email):
                                email_check1 = ["gmail", "hotmail", "yahoo", "outlook", "rediffmail"]
                                email_check2 = [".com", ".in", ".org", ".edu", ".co.in"]

                                count = 0
                                for domain in email_check1:
                                    if domain in receiver_email:
                                        count += 1
                                for site in email_check2:
                                    if site in receiver_email:
                                        count += 1

                                if "@" not in receiver_email or count != 2:
                                    print("Invalid Email ID!")
                                    new_receiver_email = input("Enter correct Email ID:")
                                    return email_verification(new_receiver_email)
                                return receiver_email

                            valid_receiver_email = email_verification(receiver_email)  # Checking if the email is valid or not

                            body = f"Dear,\n\nYour One Time Password (OTP) is {OTP}."  # Generating a message
                            subject = "One Time Password (OTP) for verification"
                            message = f'Subject: {subject}\n\n{body}'

                            server.sendmail(sender_email, valid_receiver_email, message)

                            def sending_otp(receiver_email):
                                New_OTP = random.randint(100000, 999999)

                                body = f"Dear {name},\n\nYour One Time Password (OTP) is {New_OTP}."  # Generating a message with new OTP
                                subject = "One Time Password (OTP) for verification"
                                message = f'Subject: {subject}\n\n{body}'

                                server.sendmail(sender_email, receiver_email, message)
                                print("OTP has been sent to " + receiver_email)
                                received_OTP = int(input("Enter OTP:"))

                                if received_OTP == New_OTP:  # Verifying the entered OTP
                                    print("OTP Verified! , Enter Aadhaar Number now:")
                                else:
                                    print("Invalid OTP!")
                                    print("Resending OTP...")
                                    sending_otp(receiver_email)

                            print("OTP has been sent to " + valid_receiver_email)
                            received_OTP = int(input("Enter OTP:"))

                            if received_OTP == OTP:  # Verifying the entered OTP
                                otp_verified = True
                                return "OTP Verified!, Enter Aadhaar Number now:"
                            else:
                                print("Invalid OTP!")
                                answer = input("Enter Yes to resend OTP to the same Email ID and No to enter a new Email ID:")
                                YES = ["YES", "yes", "Yes"]
                                NO = ["NO", "no", "No"]
                                if answer in YES:
                                    sending_otp(valid_receiver_email)
                                elif answer in NO:
                                    new_receiver_email = input("Enter new Email ID:")
                                    valid_receiver_email = email_verification(new_receiver_email)
                                    sending_otp(valid_receiver_email)
                                else:
                                    print("Invalid Input!")

                    except smtplib.SMTPException as e:
                        print(f"SMTP error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                elif tag == "aadhar_number":
                    if otp_verified:
                        return "Please verify your OTP before entering the Aadhaar number."
                    user_data["aadhar_id"] = msg.split("Aadhar number is")[-1].strip()
                    return "Aadhar number received. Let's proceed with the payment. Please confirm if you want to pay now."

                elif tag == "payment":
                        return "Redirecting to payment gateway... Once payment is successful, you will receive your booking confirmation."
                
                elif tag == "confirmation":
                    # Generate QR code for confirmation
                    confirmation_data = f"Booking Confirmed!\nName: {user_data['name']}\nMuseum: {user_data['museum_name']}\nVisit Date: {user_data['visit_date']}\nTotal Cost: ${user_data.get('total_cost', 0):.2f}"
                    qr_filename = generate_qr_code(confirmation_data)
                    return f"Your booking is confirmed! Here is your QR code:\n{qr_filename}"

                return random.choice(intent['responses'])
        return "Sorry, I didn't get that. Could you please rephrase your question?"

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    response = get_response(user_input)
    print(f"{bot_name}: {response}")
