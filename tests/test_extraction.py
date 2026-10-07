from pathlib import Path
from tempfile import TemporaryDirectory

import pymupdf
from docx import Document as DocxDocument

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


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        test_txt_extraction(directory)
        test_docx_extraction(directory)
        test_pdf_extraction(directory)

    print("\nAll extraction tests passed!")
