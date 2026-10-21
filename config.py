# config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram
    bot_token: str
    admin_chat_id: int | None = None

    # Пути
    upload_dir: Path = Path("uploads")
    max_file_size_mb: int = 20

    # Paperlayer
    paperlayer_table_mode: str = "markdown"
    paperlayer_keep_headers: bool = False


# Singleton — импортируется везде, где нужны настройки
settings = Settings()
