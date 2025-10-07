from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import re


def clean_and_format_text(content: str) -> str:
    """
    Cleans markdown-style text and converts **bold** to <b>bold</b> for PDF rendering.
    Converts lines starting with ### into <b><u>subheadings</u></b>.
    Also replaces ■ with • and normalizes paragraph spacing.
    """

    # Normalize line endings and trim leading/trailing spaces
    content = content.strip().replace("\r\n", "\n")

    # Convert **bold** syntax to <b></b>
    content = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", content)

    # Replace ■ with bullet symbol
    content = content.replace("■", "•")

    # Convert lines starting with ### into subheadings
    def subheading_replacer(match):
        heading_text = match.group(1).strip()
        return f"<br/><b><u>{heading_text}</u></b><br/>"

    content = re.sub(r"^###\s*(.*)$", subheading_replacer, content, flags=re.MULTILINE)

    # Normalize multiple blank lines → paragraph breaks
    content = re.sub(r"\n\s*\n", "<br/><br/>", content)

    # Replace single newlines (inside paragraphs) with <br/> for inline formatting
    content = re.sub(r"(?<!<br/>)\n(?!<br/>)", "<br/>", content)

    return content


def create_pdf_from_string(content: str, title: str = "Generated Report", filename: str = "output.pdf") -> str:
    """
    Converts plain text or multi-line string into a structured PDF.

    Args:
        content (str): Text content to be parsed into the PDF.
        title (str): Title of the document.
        filename (str): Name of the output PDF file.

    Returns:
        str: Path to the generated PDF file.
    """
    # Initialize PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50
    )

    # Clean and format text
    formatted_content = clean_and_format_text(content)

    # Set up styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=4, leading=15))  # Justified paragraphs
    styles.add(ParagraphStyle(name="CustomTitle", parent=styles["Heading1"], spaceAfter=12))

    story = []

    # Title section
    story.append(Paragraph(title, styles["CustomTitle"]))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Split into paragraphs by <br/><br/> markers (from cleaner)
    paragraphs = formatted_content.split("<br/><br/>")
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles["Justify"]))
            story.append(Spacer(1, 0.15 * inch))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF generated successfully: {filename}")
    return filename


if __name__ == "__main__":
    sample_text = """
    **Comprehensive Improvement Plan for the Store Based on Predicted Quantity Sold**
    The predictive sales figures for the two flagship products in the two key urban markets—Rice (10 kg) in Ikeja,
    Lagos and Milk (1 L) in Wuse, Abuja—indicate that the store’s current inventory mix, marketing focus, and
    staffing allocation do not fully capture the underlying demand patterns.

    1. **Inventory Alignment**
    * **Stock■level optimization:**
    - Raise the safety stock of Rice (10 kg) in Ikeja to reflect a predicted sales volume of 7.38 units per period.
    """

    create_pdf_from_string(sample_text, title="Store Improvement Report", filename="improvement_plan.pdf")
