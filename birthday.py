import smtplib
import sched
import time
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env in project root
load_dotenv()

# Email credentials
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")

if not email_user or not email_pass:
    print("❌ Email credentials not loaded. Check your .env file.")
    exit()

# Email subject
subject = "🎉 HAPPY BIRTHDAY 🎉"

# Email schedule list
email_schedule = [
    {
        'email': 'pujamg2020@gmail.com',
        'date': '23-04-2025',
        'time': '21:55',
        'message': 'DEAR PUJA, \nwishing you a day full of love and joy. Happy Birthday!'
    },
    {
        'email': 'gaikwadumesh123@gmail.com',
        'date': '17-01-2026',
        'time': '00:01',
        'message': 'DEAR UMESH, \nwishing you a day full of love and joy. Happy Birthday!'
    },
    {
        'email': '1marotigaikwad@gmail.com',
        'date': '04-06-2025',
        'time': '00:01',
        'message': 'DEAR ANNA, \nwishing you a day full of love and joy. Happy Birthday!'
    },
    {
        'email': 'mangeshgayakwad2020@gmail.com',
        'date': '02-02-2026',
        'time': '00:01',
        'message': 'DEAR MANGESH, \nwishing you a day full of love and joy. Happy Birthday!'
    },
    {
        'email': '1marotigaikwad@gmail.com',
        'date': '01-01-2026',
        'time': '00:01',
        'message': 'DEAR MUMMY, \nwishing you a day full of love and joy. Happy Birthday!'
    }
]

# Create scheduler
email_scheduler = sched.scheduler(time.time, time.sleep)


# Send email function
def send_mail(to_email, message_text, scheduled_for):
    try:
        msg = MIMEText(f"{message_text}\n\nScheduled on: {scheduled_for}")
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email} at {scheduled_for}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication error: Check your email or app password.")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")


# Schedule email function
def schedule_email(email_info):
    try:
        date_str = email_info['date']
        time_str = email_info['time']
        schedule_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
        now = datetime.now()
        delay = (schedule_time - now).total_seconds()

        if delay > 0:
            print(f"🕒 Scheduling email to {email_info['email']} at {schedule_time}")
            email_scheduler.enter(delay, 1, send_mail, argument=(
                email_info['email'],
                email_info['message'],
                f"{date_str} {time_str}"
            ))
        else:
            print(f"⚠️ Skipped {email_info['email']} - Time already passed.")
    except Exception as e:
        print(f"❌ Error scheduling for {email_info['email']}: {e}")


# Schedule all emails
for email_info in email_schedule:
    schedule_email(email_info)

print("📅 All emails scheduled. Waiting to send...")
email_scheduler.run()
