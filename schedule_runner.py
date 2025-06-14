#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import logging
from datetime import datetime, timezone

# Конфигурация (можно менять)
SCHEDULE_TIMES = ["21:28"]  # UTC время загрузки (3 раза в день)
PIPELINE_SCRIPT = "run_pipeline.py"  # Ваш основной скрипт
LOG_FILE = "/tmp/pipeline_scheduler.log"  # Логи будут доступны в Console

# Проверка критических переменных окружения
REQUIRED_ENV_VARS = [
    'OPENAI_API_KEY',
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_ID',
    'YOUTUBE_API_KEY'
]

# Настройка продвинутого логгирования
class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Консольный вывод с цветами
ch = logging.StreamHandler()
ch.setFormatter(ColorFormatter())
logger.addHandler(ch)

# Файловый лог (для Render Console)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(fh)

def validate_environment():
    """Проверяет обязательные переменные окружения"""
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        logger.critical(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        sys.exit(1)
    
    logger.info("✅ Все переменные окружения доступны")
    logger.debug(f"Telegram Chat ID: {os.getenv('TELEGRAM_CHAT_ID')}")
    logger.debug(f"YouTube API Key: {os.getenv('YOUTUBE_API_KEY')[:5]}...")

def run_pipeline():
    """Запускает основной пайплайн с обработкой ошибок"""
    try:
        logger.info("🚀 Запускаю пайплайн обработки видео")
        
        # Явный запуск через системный Python
        result = subprocess.run(
            [sys.executable, PIPELINE_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3600,  # 1 час таймаут
            check=True
        )
        
        logger.info(f"✅ Успешно завершено\nOutput: {result.stdout[:300]}...")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("🕒 Пайплайн превысил лимит времени (1 час)")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Ошибка выполнения (код {e.returncode})\nError: {e.stderr[:300]}...")
    except Exception as e:
        logger.error(f"🔥 Непредвиденная ошибка: {str(e)}", exc_info=True)
    
    return False

def send_telegram_notification(message: str):
    """Отправляет уведомление в Telegram"""
    try:
        from notifier import send_message
        send_message(message)
    except Exception as e:
        logger.warning(f"⚠️ Не удалось отправить в Telegram: {str(e)}")

def main():
    """Основной цикл выполнения"""
    validate_environment()
    
    logger.info(f"⏰ Планировщик запущен (Python {sys.version})")
    logger.info(f"🔄 Расписание: {', '.join(SCHEDULE_TIMES)} UTC")
    send_telegram_notification("🔄 Планировщик видео запущен")
    
    # Тестовый запуск
    logger.info("🧪 Выполняю тестовый запуск...")
    if run_pipeline():
        send_telegram_notification("✅ Тестовый запуск успешен")
    else:
        send_telegram_notification("❌ Тестовый запуск не удался")
    
    # Основной цикл
    while True:
        try:
            current_time = datetime.now(timezone.utc).strftime("%H:%M")
            logger.debug(f"Проверка расписания (UTC: {current_time})")
            
            if current_time in SCHEDULE_TIMES:
                send_telegram_notification(f"⏳ Начинаю обработку видео ({current_time} UTC)")
                
                if run_pipeline():
                    send_telegram_notification("✅ Видео успешно обработано")
                    time.sleep(3600)  # Защита от повтора
                else:
                    time.sleep(600)  # При ошибке ждем 10 минут
            
            time.sleep(30)  # Проверка каждые 30 секунд
            
        except KeyboardInterrupt:
            logger.info("🛑 Остановка по запросу пользователя")
            break
        except Exception as e:
            logger.error(f"💀 Критическая ошибка: {str(e)}", exc_info=True)
            time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"💥 Фатальная ошибка: {str(e)}", exc_info=True)
        send_telegram_notification(f"💥 Планировщик упал: {str(e)}")
        sys.exit(1)
