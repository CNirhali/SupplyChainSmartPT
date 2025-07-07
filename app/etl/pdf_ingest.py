from PyPDF2 import PdfReader
from io import BytesIO

def extract_pdf_text(file: BytesIO) -> str:
    """
    Extract text from all pages of a PDF file (BytesIO) and return as a single string.
    Args:
        file (BytesIO): The uploaded PDF file.
    Returns:
        str: Concatenated text from all pages.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text 