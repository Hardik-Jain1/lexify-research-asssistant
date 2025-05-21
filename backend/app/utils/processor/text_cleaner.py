import re
import ftfy
from typing import List

class TextCleaner:
    def __init__(self):
        pass

    def clean(self, text: str) -> str:
        """
        Cleans raw extracted text from a research paper PDF.
        - Fixes unicode issues
        - Removes headers, footers, and page numbers
        - Normalizes line breaks
        - Removes inline citations and references
        - Fixes special characters
        - Normalizes section titles and retains newlines
        - Removes redundant content
        """
        # Fix unicode issues
        text = ftfy.fix_text(text)

        # Remove headers, footers, and page numbers
        text = re.sub(r'\n\d+\n', '\n', text)  # Standalone page numbers
        text = re.sub(r'arXiv:\d+\.\d+v\d+ \[.*?\] \d{1,2} \w{3} \d{4}', '', text)  # arXiv metadata

        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n', text)  # Collapse multiple newlines
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = re.sub(r'\n(?=[a-z])', ' ', text)  # Fix broken lines

        # Remove inline citations and references
        text = re.sub(r'\[\d+\]', '', text)  # Inline citations
        text = re.sub(r'\(.*?\)', '', text)  # Parenthetical references

        # Fix special characters
        text = re.sub(r'\f', '', text)  # Remove form feed characters
        text = re.sub(r'-{2,}', '', text)  # Remove horizontal rules

        # Normalize section titles and retain newlines
        text = re.sub(r'^(\d+\.\s+)', '\n', text, flags=re.MULTILINE)  # Remove numbering and add newline
        text = re.sub(r'^(\d+\.\d+\.\s+)', '\n', text, flags=re.MULTILINE)  # Subsection numbering
        text = re.sub(r'^(\d+\.\d+\.\d+\.\s+)', '\n', text, flags=re.MULTILINE)  # Sub-subsection numbering
        text = re.sub(r'^(\s*[A-Z][a-zA-Z ]+\n)', lambda m: '\n' + m.group(0).strip().title() + '\n', text, flags=re.MULTILINE)  # Title case section titles

        # Remove redundant content
        text = re.sub(r'Figure \d+:.*?\n', '', text)  # Remove figure captions
        text = re.sub(r'Table \d+:.*?\n', '', text)  # Remove table captions
        text = re.sub(r'\nKey Words:.*?\n', '\n', text, flags=re.IGNORECASE)  # Remove keywords section

        return text.strip()

    def clean_bulk(self, texts: List[str]) -> List[str]:
        return [self.clean(text) for text in texts]