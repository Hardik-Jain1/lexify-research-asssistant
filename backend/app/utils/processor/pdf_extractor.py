import fitz  # PyMuPDF
from pathlib import Path
from typing import Union

def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extracts raw text from a PDF using PyMuPDF (fitz).
    Returns all pages concatenated into a single string.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()
    except Exception as e:
        raise RuntimeError(f"Error extracting PDF text: {e}")

    return text.strip()