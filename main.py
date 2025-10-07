from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import EmailStr
import os
import shutil
from models.inference import run_inference
from models.NLP import generate_response
from utils.pdf_generator import create_pdf_from_string
# from utils.send_email import send_email_with_pdf
from dotenv import load_dotenv
import re
from html import escape

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure uploads folder exists


@app.post("/analyze")
async def analyze_data(
    file: UploadFile = File(...),
    store_name: str = Form(...),
    email: EmailStr = Form(...)
):
    """
    Analyzes uploaded sales data, generates insights,
    converts them to a PDF, and returns the PDF file.
    """

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 1: Run inference (predictive model)
    prediction = run_inference(file_path)

    # Step 2: Generate NLP insights
    insights = generate_response(f"Analyze the following sales data and provide insights: {prediction}")

    # Step 3: Generate a PDF report
    pdf_filename = f"{store_name.replace(' ', '_')}_Sales_Report.pdf"
    pdf_path = create_pdf_from_string(
        content=sanitize_text(insights),
        title=f"{store_name} Sales Report",
        filename=pdf_filename
    )

    # # Step 4: (Optional) Send Email with attachment
    # send_email_with_pdf(
    #     sender_email=os.getenv("SENDER_EMAIL"),
    #     sender_password=os.getenv("SENDER_PASSWORD"),
    #     recipient_email=email,
    #     subject=f"{store_name} - Sales Report",
    #     body=f"Hello {store_name},\n\nPlease find attached your generated sales report.\n\nBest regards,\nThe Analytics Team",
    #     pdf_path=pdf_path
    # )

    # ✅ Return the generated PDF file for download
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )


def sanitize_text(text: str) -> str:
    """
    Clean and normalize the text for ReportLab Paragraph.
    Converts <br> to <br/> and removes unsupported tags.
    """
    if not text:
        return ""

    text = text.replace("<br>", "<br/>").replace("\n", "<br/>")

    allowed_tags = ["<b>", "</b>", "<i>", "</i>", "<u>", "</u>", "<br/>", "<para>", "</para>"]

    def escape_except_allowed(match):
        tag = match.group(0)
        return tag if tag in allowed_tags else escape(tag)

    text = re.sub(r"<.*?>", escape_except_allowed, text)
    return text

