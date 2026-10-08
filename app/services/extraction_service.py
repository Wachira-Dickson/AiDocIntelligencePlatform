import io
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image
from docx import Document as DocxDocument

def extract_text_from_pdf(file_path) -> str:
    extracted_pages = []

    with pymupdf.open(file_path) as document:
        for page in document:
            #Try normal PDF text extraction first.
            text = page.get_text("text").strip()

            #If the page has little or no selectable text, use OCR.
            if len(text) < 20:
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False,
                )

                image_bytes = pixmap.tobytes("png")
                image = Image.open(io.BytesIO(image_bytes))

                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                ).strip()

            extracted_pages.append(text)
        
        return "\n\n".join(extracted_pages).strip()

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