# ocr.py
"""
OCR для PDF-сканов без текстового слоя.
Требует: tesseract-ocr, poppler-utils (системные пакеты).
"""
import logging

import pytesseract
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

# Путь к Tesseract (если не в PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Путь к Poppler (если не в PATH)
POPPLER_PATH = r"C:\Program Files\Poppler\poppler-26.09.0\Library\bin"


def is_available() -> bool:
    """Проверить, установлен ли Tesseract."""
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def pdf_to_text(
    file_path: str,
    lang: str = "eng+rus",
    dpi: int = 300,
    max_pages: int = 50,
) -> str:
    """
    Извлекает текст из PDF-скана через OCR.

    Args:
        file_path: путь к PDF
        lang: языки Tesseract ("eng+rus" — английский + русский)
        dpi: разрешение рендера (300 — стандарт для OCR)
        max_pages: лимит страниц (защита от гигантских PDF)
    """
    if not is_available():
        raise RuntimeError(
            "Tesseract не установлен. Установите: "
            "https://github.com/UB-Mannheim/tesseract/wiki"
        )

    logger.info(f"OCR started: {file_path}, lang={lang}, dpi={dpi}")

    # ОДИН вызов convert_from_path — со всеми параметрами
    images = convert_from_path(
        file_path,
        dpi=dpi,
        first_page=1,
        last_page=max_pages,
        poppler_path=POPPLER_PATH,
    )

    pages_text = []
    for i, image in enumerate(images, start=1):
        logger.debug(f"OCR page {i}/{len(images)}")
        text = pytesseract.image_to_string(image, lang=lang)
        if text.strip():
            pages_text.append(f"## Page {i}\n\n{text.strip()}")

    result = "\n\n".join(pages_text)
    logger.info(f"OCR done: {len(images)} pages, {len(result)} chars")
    return result
