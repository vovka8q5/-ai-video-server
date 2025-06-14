# run_pipeline.py
import os
import time
from notifier import send_message

def run_pipeline():
    send_message("🎬 Начинаем обработку видео")
    print("🎬 Запуск пайплайна...")

    # Здесь может быть реальная логика: скачивание, стилизация, субтитры, публикация
    time.sleep(5)  # Заглушка обработки

    print("✅ Обработка завершена")
    send_message("✅ Видео загружено и опубликовано")

if __name__ == "__main__":
    run_pipeline()
