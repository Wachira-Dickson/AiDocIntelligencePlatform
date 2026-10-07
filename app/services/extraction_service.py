from pathlib import Path

import pymupdf
from docx import Document as DocxDocument

def extract_text_from_pdf(file_path) -> str:
    text = []

    with pymupdf.open(file_path) as document:
        for page in document:
            text.append(page.get_text())

    return "\n".join(text).strip()

def extract_text_from_docx(file_path: str) -> str:
    document = DocxDocument(file_path)

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    return "\n".join(paragraphs).strip()

def extract_text_from_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8").strip()

def extract_text(file_path: str, content_type: str) -> str:
    if content_type == "application/pdf":
        return extract_text_from_pdf(file_path)
    
    if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_path)
    
    if content_type == "text/plain":
        return extract_text_from_txt(file_path)
    
    raise ValueError(f"Unsupported document type: {content_type}")