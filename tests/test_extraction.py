from pathlib import Path
from tempfile import TemporaryDirectory

import pymupdf
from docx import Document as DocxDocument
from PIL import Image, ImageDraw, ImageFont

from app.services.extraction_service import extract_text


def test_txt_extraction(directory: Path):
    file_path = directory / "sample.txt"
    file_path.write_text("This is a TXT extraction test.", encoding="utf-8")

    text = extract_text(str(file_path), "text/plain")
    assert text == "This is a TXT extraction test."
    print("TXT extraction: PASSED")


def test_docx_extraction(directory: Path):
    file_path = directory / "sample.docx"

    document = DocxDocument()
    document.add_paragraph("This is a DOCX extraction test.")
    document.save(file_path)

    content_type = (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    )
    text = extract_text(str(file_path), content_type)

    assert text == "This is a DOCX extraction test."
    print("DOCX extraction: PASSED")


def test_pdf_extraction(directory: Path):
    file_path = directory / "sample.pdf"

    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), "This is a PDF extraction test.")
        document.save(file_path)

    text = extract_text(str(file_path), "application/pdf")

    assert "This is a PDF extraction test." in text
    print("PDF extraction: PASSED")

def test_scanned_pdf_ocr(directory: Path):
    image_path = directory / "scanned_page.png"
    pdf_path = directory / "scanned.pdf"

    #Create an image containing text, simulating a scanned page.
    image = Image.new("RGB", (1200, 300), "white")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        40,
    )

    draw.text(
        (40, 100),
        "OCR extraction test document",
        fill="black",
        font=font,
    )
    image.save(image_path)

    #Put the image into a PDF without an underlying text layer
    with pymupdf.open() as document:
        page = document.new_page(width=600, height=150)
        page.insert_image(page.rect, filename=str(image_path))
        document.save(pdf_path)

    text = extract_text(str(pdf_path), "application/pdf")

    assert "OCR extraction test document" in text, (
        f"OCR did not recover the expected text. Extracted: {text!r}"
    )
    print("Scanned PDF OCR: PASSED")


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        test_txt_extraction(directory)
        test_docx_extraction(directory)
        test_pdf_extraction(directory)
        test_scanned_pdf_ocr(directory)

    print("\nAll extraction tests passed!")
