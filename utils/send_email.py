"""
Email Sender Module
-------------------
Sends an email with a PDF attachment.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_pdf(sender_email, sender_password, recipient_email, subject, body, pdf_path):
    """
    Sends an email with a PDF attachment using SMTP.

    Args:
        sender_email (str): The sender's email address.
        sender_password (str): The sender's email password or app-specific password.
        recipient_email (str): Recipient email address.
        subject (str): Email subject line.
        body (str): Email body text.
        pdf_path (str): Path to the PDF file to attach.
    """
    # Build email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF file
    with open(pdf_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename=pdf_path)
        msg.attach(pdf_attachment)

    # Send via SMTP (Gmail example)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

    print(f"📧 Email sent successfully to {recipient_email}")
