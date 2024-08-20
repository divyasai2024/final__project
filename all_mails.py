import smtplib
import os
import schedule
import time
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

os.chdir(r"C:\demopython\send_mail")

# Function to fetch email data from the database
def fetch_email_data():
    # Connect to the SQLite database (replace with your database connection if using another DB)
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT recipient_email, subject, body FROM emails")  # Adjust the query as needed
    email_data = cursor.fetchall()  # Fetch all rows
    
    conn.close()
    
    return email_data  # Return the list of email data

# Function to send email
def send_email():
    email_data_list = fetch_email_data()
    
    if not email_data_list:
        print("No email data found.")
        return

    from_email = 'vtechprojectmail@gmail.com'

    # Email server credentials
    email_server = 'smtp.gmail.com'
    email_port = 587
    email_user = 'vtechprojectmail@gmail.com'
    email_password = 'ttnftyfthdlaoohy'

    for email_data in email_data_list:
        recipient_email, subject, body = email_data

        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the server and send the email
        try:
            server = smtplib.SMTP(email_server, email_port)
            server.starttls()
            server.login(email_user, email_password)
            text = msg.as_string()
            server.sendmail(from_email, recipient_email, text)
            print(f"Email sent to {recipient_email} successfully!")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
        finally:
            server.quit()

# Schedule the email
schedule.every().day.at("22:45").do(send_email)  # Change the time as needed

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
