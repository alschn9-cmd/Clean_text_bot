# processor.py

import logging 

from paperlayer import parse
from ocr import pdf_to_text

logger = logging.getLogger(__name__)

def pdf_to_markdown(file_path: str) -> str:
    # 1. Пробуем paperlayer (быстро, без OCR)
    doc = parse(file_path, table_mode="markdown", keep_headers=False)
    lines = [block.markdown for block in doc.blocks if block.type in ("heading", "paragraph", "list", "table", "caption")]
    markdown = "\n\n".join(lines)

    # 2. Если текста нет — это скан, запускаем OCR
    if not markdown.strip():
        logger.warning(f"paperlayer returned empty for {file_path}, trying OCR")
        markdown = pdf_to_text(file_path)

    return markdown
