# app/core/processing_service.py
from flask import current_app
from pathlib import Path
# Assuming processor.pdf_extractor and processor.text_cleaner are accessible
from app.utils.processor.pdf_extractor import extract_text_from_pdf as extract_text_external
from app.utils.processor.text_cleaner import TextCleaner # Your TextCleaner is a class

# Initialize cleaner once, or make its methods static if no state is stored
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
        except RuntimeError as e: # Catching specific error from your extractor
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
            # Return raw text or empty string on failure, or raise
            return raw_text # Or raise, depending on desired behavior