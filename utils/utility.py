"""
Main script to generate a PDF from a string and send it by email.
"""

from pdf_generator import create_pdf_from_string
from send_email import send_email_with_pdf

if __name__ == "__main__":
    # Step 1: Your report or message as text
    report_text = """
    Sales Summary Report - Q4 2025

    Total Revenue: $120,500
    Total Expenses: $83,200
    Net Profit: $37,300

    Highlights:
    - Online sales grew by 25%.
    - Customer retention improved by 12%.
    - Africa and Europe markets led in growth.
    """

    # Step 2: Generate PDF
    pdf_path = create_pdf_from_string(report_text, title="Q4 Sales Report", filename="Q4_Sales_Report.pdf")

    # Step 3: Send Email
    send_email_with_pdf(
        sender_email="youremail@gmail.com",
        sender_password="your-app-password",  # Use an app-specific password, not your Gmail password
        recipient_email="recipient@example.com",
        subject="Q4 2025 Sales Report",
        body="Hello,\n\nPlease find attached the Q4 Sales Report PDF.\n\nBest regards,\nYour Team",
        pdf_path=pdf_path
    )
