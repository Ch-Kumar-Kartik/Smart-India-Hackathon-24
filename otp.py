import random
import smtplib

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

        name = input("Enter your name:")
        receiver_email = input("Enter your Email ID:")

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

        body = f"Dear {name},\n\nYour One Time Password (OTP) is {OTP}."  # Generating a message
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
                print("OTP Verified!")
            else:
                print("Invalid OTP!")
                print("Resending OTP...")
                sending_otp(receiver_email)

        print("OTP has been sent to " + valid_receiver_email)
        received_OTP = int(input("Enter OTP:"))

        if received_OTP == OTP:  # Verifying the entered OTP
            print("OTP Verified!")
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
