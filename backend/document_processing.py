import io
import os

import pdfplumber

try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None


def extract_document_text(filename, file_bytes):
    text_content = ""
    ocr_text = ""
    extraction_method = "text"

    lowered = filename.lower()

    if lowered.endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    if page_text:
                        text_content += page_text + "\n"
        except Exception:
            text_content = ""

        if not text_content.strip():
            extraction_method = "none"
    elif lowered.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        ocr_text = _ocr_image_bytes(file_bytes)
        extraction_method = "ocr" if ocr_text.strip() else "none"
    else:
        text_content = _decode_text(file_bytes)
        extraction_method = "text" if text_content.strip() else "none"

    combined_text = text_content.strip() if text_content.strip() else ocr_text.strip()

    return {
        "combined_text": combined_text,
        "text_content": text_content,
        "ocr_text": ocr_text,
        "extraction_method": extraction_method
    }


def _decode_text(file_bytes):
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        try:
            return file_bytes.decode("latin-1", errors="ignore")
        except Exception:
            return ""


def _configure_tesseract():
    if pytesseract is None:
        return
    tesseract_cmd = os.getenv("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def _ocr_image_bytes(file_bytes):
    if Image is None or pytesseract is None:
        return ""

    try:
        _configure_tesseract()
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
    except Exception:
        return ""
