import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import pandas as pd
import base64

def prepareExcel(data):
    # Assuming data is a list of dictionaries
    print(data)
    df = pd.DataFrame(data)
    excel_file = './data.xlsx'
    df.to_excel(excel_file, index=False)
    print("Excel Creation Successful")
    return excel_file

def send_email(recipient, subject, body, attachment=None):
    sender_email = "sathishtitan@yahoo.com"  # Replace with your email address
    password = "Kumarbrothers@2001"  # Replace with your email password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if attachment:
        print("Attachment Available")
        try:
            attachment_data = base64.b64decode(attachment)
            with open("./data.xlsx", "wb") as attachment_file:
                attachment_file.write(attachment_data)
            with open("attachment.xlsx", "rb") as attachment_file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {attachment}")
                message.attach(part)
        except FileNotFoundError:
            print("Attachment file not found.")
        except Exception as e:
            print(f"Error attaching file: {e}")

    # Use smtplib.SMTP_SSL for enhanced security (recommended)
    with smtplib.SMTP_SSL("smtp.yahoo.com", 465) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, [recipient], message.as_string())
            print('Login Successful and Email Sent Successful')
        except Exception as e:
            print(f"Error sending email: {e}")
