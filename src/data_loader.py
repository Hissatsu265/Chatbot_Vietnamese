import os
from PyPDF2 import PdfReader

def load_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages])

def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
