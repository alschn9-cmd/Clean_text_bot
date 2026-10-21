# html_processor.py
import logging
import re
from pathlib import Path
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Теги, которые удаляем целиком (навигация, скрипты и т.д.)
REMOVE_TAGS = [
    "script", "style", "noscript", "iframe", "nav", "footer", "header", 
    "aside", "form", "button", "svg", "canvas",
]

# Классы и ID, которые обычно содержат «хром» сайта
REMOVE_PATTERNS = re.compile(
    r"(nav|menu|footer|header|sidebar|breadcrumb|crumb|cookie|banner|"
    r"popup|modal|social|share|advert|ads?|related|recommend|comment|"
    r"common-side|side-pro)",
    re.IGNORECASE,
)

def clean_soup(soup: BeautifulSoup) -> BeautifulSoup:
    """Удаляет теги и блоки, которые не нужны для RAG."""
    for tag in REMOVE_TAGS:
        for el in soup.find_all(tag):
            el.decompose()
            
    for el in soup.find_all(attrs={"class": REMOVE_PATTERNS}):
        el.decompose()
    for el in soup.find_all(attrs={"id": REMOVE_PATTERNS}):
        el.decompose()
        
    return soup

def expand_rowspan_tables(soup: BeautifulSoup) -> BeautifulSoup:
    """Исправляет таблицы с rowspan, дублируя значения первой колонки."""
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
            
        active_rowspans = {}
        for row in rows:
            cells = row.find_all(["td", "th"])
            col_index = 0
            for cell in cells:
                while col_index in active_rowspans:
                    value, remaining = active_rowspans[col_index]
                    new_cell = soup.new_tag("td")
                    new_cell.string = value
                    cell.insert_before(new_cell)
                    col_index += 1
                    if remaining - 1 <= 0:
                        del active_rowspans[col_index - 1]
                    else:
                        active_rowspans[col_index - 1] = (value, remaining - 1)
                        
                rowspan = int(cell.get("rowspan", 1))
                if rowspan > 1:
                    active_rowspans[col_index] = (cell.get_text(strip=True), rowspan - 1)
                col_index += 1
    return soup

def _table_to_markdown(table) -> str:
    """Конвертирует HTML-таблицу в Markdown."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        # Пропускаем строки, где меньше 2 ячеек (артефакты rowspan)
        if len(cells) > 1:
            rows.append(cells)
            
    if not rows:
        return ""
        
    header = rows[0]
    separator = ["---"] * len(header)
    body = rows[1:]
    
    md = ["| " + " | ".join(header) + " |"]
    md.append("| " + " | ".join(separator) + " |")
    for row in body:
        # Выравниваем длину строки под заголовок
        row = (row + [""] * len(header))[: len(header)]
        md.append("| " + " | ".join(row) + " |")
        
    return "\n".join(md)

def container_to_markdown(container) -> str:
    """Превращает контейнер в Markdown, собирая только нужные элементы."""
    lines = []

    # Ищем заголовки, параграфы, списки и таблицы
    for el in container.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "table", "article"]
    ):
        # Если это article, и внутри него есть p — пропускаем его (чтобы не было дублей)
        if el.name == "article" and el.find("p"):
            continue

        text = el.get_text(" ", strip=True)
        
        if not text or (el.name == "p" and len(text) < 2):
            continue

        if el.name == "h1":
            lines.append(f"# {text}")
        elif el.name == "h2":
            lines.append(f"## {text}")
        elif el.name == "h3":
            lines.append(f"### {text}")
        elif el.name in ("h4", "h5", "h6"):
            lines.append(f"#### {text}")
        elif el.name == "li":
            lines.append(f"- {text}")
        elif el.name == "p":
            lines.append(text)
        elif el.name == "article": # ← ДОБАВЛЕНО СЮДА
            lines.append(text) 
        elif el.name == "table":
            lines.append("\n" + _table_to_markdown(el) + "\n")

    return "\n\n".join(line.strip() for line in lines if line.strip())

def extract_content(soup: BeautifulSoup) -> str:
    """Собирает Markdown из главного контейнера страницы."""
    # Берем главный контейнер страницы товара
    container = soup.select_one(".pro-detail-wrap")
    
    if not container:
        logger.warning("Main container not found, trying fallback")
        container = soup.body
        
    if not container:
        return ""

    # Очищаем контейнер от мусора ПЕРЕД парсингом (на всякий случай)
    for el in container.select(".common-side, .feedback, .share-btn-list, .btn-list"):
        el.decompose()

    return container_to_markdown(container)

def html_file_to_markdown(file_path: str) -> str:
    """Главная функция: читает HTML-файл и возвращает Markdown."""
    path = Path(file_path)
    html = path.read_text(encoding="utf-8", errors="replace")
    
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Убираем мусор (скрипты, стили, навигацию)
    soup = clean_soup(soup)
    
    # 2. Исправляем таблицы ДО парсинга
    soup = expand_rowspan_tables(soup) 
    
    # 3. Извлекаем контент
    markdown = extract_content(soup)
    
    logger.info(f"html_file_to_markdown: {len(html)} → {len(markdown)} chars")
    return markdown
