from flask import current_app
from pathlib import Path
from app.utils.processor.pdf_extractor import extract_text_from_pdf as extract_text_external
from app.utils.processor.text_cleaner import TextCleaner

text_cleaner_instance = TextCleaner()

class ProcessingService:
    @staticmethod
    def extract_text(pdf_path: str) -> str | None:
        """Extracts text from a given PDF path."""
        try:
            text = extract_text_external(pdf_path)
            return text
        except FileNotFoundError:
            current_app.logger.error(f"PDF not found for extraction: {pdf_path}")
            return None
        except RuntimeError as e:
            current_app.logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return None
        except Exception as e:
            current_app.logger.error(f"Unexpected error extracting text from PDF {pdf_path}: {e}")
            return None

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """Cleans the extracted text."""
        try:
            cleaned_text = text_cleaner_instance.clean(raw_text)
            return cleaned_text
        except Exception as e:
            current_app.logger.error(f"Error cleaning text: {e}")
            return raw_text