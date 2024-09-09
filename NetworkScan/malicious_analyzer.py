import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Directory for malicious logs
MALICIOUS_LOG_DIR = "MaliciousLogFile"

# Email settings
SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
SMTP_PORT = 587
SMTP_USERNAME = "karanchavda953@gmail.com"  # Replace with your email
SMTP_PASSWORD = "kzcp ylxl uipy dnko"  # Replace with your email password
EMAIL_FROM = SMTP_USERNAME
EMAIL_TO = "210303108068@paruluniversity.ac.in"

def get_latest_malicious_log():
    """Get the latest malicious log file from the directory."""
    log_files = [f for f in os.listdir(MALICIOUS_LOG_DIR) if f.endswith('.log')]
    if not log_files:
        return None
    latest_log_file = max(log_files, key=lambda f: os.path.getctime(os.path.join(MALICIOUS_LOG_DIR, f)))
    return os.path.join(MALICIOUS_LOG_DIR, latest_log_file)

def generate_report(log_file_path):
    """Generate a report from the malicious log file."""
    report = []
    report.append("Malicious Packet Report\n")
    report.append("Generated on: {}\n".format(datetime.datetime.now()))
    report.append("Threat Summary:\n")
    
    with open(log_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            report.append(line)
    
    return "\n".join(report)

def send_email(report):
    """Send the report via email."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = 'Malicious Packet Detection Report'

    # Attach the report to the email
    msg.attach(MIMEText(report, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")

def main():
    latest_log_file = get_latest_malicious_log()
    if latest_log_file:
        print(f"Reading from log file: {latest_log_file}")
        report = generate_report(latest_log_file)
        send_email(report)
    else:
        print("No malicious log files found.")

if __name__ == "__main__":
    main()
