# bot.py
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from config import settings
from processor import pdf_to_markdown
from html_processor import html_file_to_markdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
_executor = ThreadPoolExecutor(max_workers=2)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Отправьте PDF или HTML-файл — я верну очищенный Markdown."
    )


@dp.message(F.document)
async def handle_document(message: types.Message):
    doc = message.document
    name = doc.file_name.lower()

    # Определяем тип файла
    if name.endswith(".pdf"):
        handler = pdf_to_markdown
        kind = "PDF"
    elif name.endswith((".html", ".htm")):
        handler = html_file_to_markdown
        kind = "HTML"
    else:
        await message.answer("Поддерживаются только PDF и HTML-файлы.")
        return

    # Проверка размера
    if doc.file_size > settings.max_file_size_mb * 1024 * 1024:
        await message.answer(
            f"Файл слишком большой (макс. {settings.max_file_size_mb} МБ)."
        )
        return

    # Скачиваем
    settings.upload_dir.mkdir(exist_ok=True)
    file_path = settings.upload_dir / f"{doc.file_id}_{doc.file_name}"

    try:
        await bot.download(doc, destination=file_path)
    except Exception as e:
        logger.exception(f"Download failed: {e}")
        await message.answer(f"Ошибка скачивания: {e}")
        return

    await message.answer(f"Обрабатываю {kind}...")

    # Обрабатываем в отдельном потоке
    loop = asyncio.get_running_loop()
    try:
        markdown = await loop.run_in_executor(
            _executor, handler, str(file_path)
        )
    except Exception as e:
        logger.exception(f"Processing failed: {e}")
        await message.answer(f"Ошибка обработки: {e}")
        return
    finally:
        file_path.unlink(missing_ok=True)

    if not markdown or not markdown.strip():
        await message.answer(
            "Не удалось извлечь контент.\n\n"
            "Проверьте, что файл содержит текст "
            "(а не только изображения)."
        )
        return

    # Отправка результата
    if len(markdown) > 4000:
        out_file = settings.upload_dir / f"{doc.file_id}.md"
        out_file.write_text(markdown, encoding="utf-8")
        await message.answer_document(types.FSInputFile(out_file))
        out_file.unlink(missing_ok=True)
    else:
        await message.answer(
            f"```markdown\n{markdown}\n```",
            parse_mode="Markdown",
        )


async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
