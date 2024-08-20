import smtplib
import os
import schedule
import time
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

os.chdir(r"C:\demopython\send_mail")
#os.mkdir("open")
# Function to fetch email data from the database
def fetch_email_data():
    # Connect to the SQLite database (replace with your database connection if using another DB)
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT recipient_email, subject, body FROM emails WHERE id = 2")  # Modify query as needed
    email_data = cursor.fetchone()
    
    conn.close()
    
    if email_data:
        return {
            'recipient_email': email_data[0],
            'subject': email_data[1],
            'body': email_data[2]
        }
    return None

# Function to send email
def send_email():
    email_data = fetch_email_data()
    
    if not email_data:
        print("No email data found.")
        return

    from_email = 'vtechprojectmail@gmail.com'
    to_email = email_data['recipient_email']
    subject = email_data['subject']
    body = email_data['body']

    # Email server credentials
    email_server = 'smtp.gmail.com'
    email_port = 587
    email_user = 'vtechprojectmail@gmail.com'
    email_password = 'ttnftyfthdlaoohy'

    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(email_server, email_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Schedule the email
schedule.every().day.at("22:04").do(send_email)  # Change the time as needed

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
