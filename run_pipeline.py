#!/usr/bin/env python3
# run_pipeline.py
import os
import sys
import logging
from datetime import datetime, timezone
from notifier import send_message
from download_video import download_from_youtube
from preprocess_video import convert_to_shorts_format
from stylize_video import apply_ai_style
from subtitle_generator import generate_subtitles
from upload_youtube import upload_to_youtube

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pipeline.log')
    ]
)
logger = logging.getLogger(__name__)

def log_step(step: str):
    """Логирует этап выполнения с таймстампом"""
    timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
    logger.info(f"🔄 [{timestamp}] {step}")
    send_message(f"🔄 {step}")

def run_pipeline():
    try:
        # 0. Инициализация
        log_step("Запуск пайплайна")
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Тестовое видео
        
        # 1. Скачивание
        log_step("Скачивание видео")
        raw_path = download_from_youtube(video_url)
        logger.info(f"Видео скачано: {raw_path}")

        # 2. Конвертация в Shorts
        log_step("Конвертация в Shorts")
        shorts_path = convert_to_shorts_format(raw_path)
        logger.info(f"Конвертация завершена: {shorts_path}")

        # 3. Стилизация
        log_step("Стилизация видео")
        styled_path = apply_ai_style(shorts_path)
        logger.info(f"Стилизация завершена: {styled_path}")

        # 4. Генерация субтитров
        log_step("Генерация субтитров")
        srt_path = generate_subtitles(styled_path)
        logger.info(f"Субтитры созданы: {srt_path}")

        # 5. Загрузка на YouTube
        log_step("Загрузка на YouTube")
        video_id = upload_to_youtube(styled_path)
        logger.info(f"Видео загружено, ID: {video_id}")

        # Успешное завершение
        log_step("Пайплайн успешно выполнен")
        send_message(f"✅ Видео опубликовано: https://youtu.be/{video_id}")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка пайплайна: {str(e)}", exc_info=True)
        send_message(f"🔥 Критическая ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    # Проверка переменных окружения
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'YOUTUBE_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        sys.exit(1)

    # Запуск пайплайна
    success = run_pipeline()
    sys.exit(0 if success else 1)
