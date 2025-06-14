import os
import time
import requests
from typing import Optional
from datetime import datetime

BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

def validate_telegram_credentials() -> bool:
    """Проверяет валидность учетных данных Telegram"""
    if not BOT_TOKEN:
        print("❌ Telegram Bot Token не установлен")
        return False
    
    if not CHAT_ID or not CHAT_ID.strip().isdigit():
        print("❌ Неверный Chat ID. Должен быть числовым значением")
        return False
    
    return True

def send_message(text: str, max_retries: int = 3) -> bool:
    """
    Отправляет сообщение в Telegram чат
    :param text: Текст сообщения
    :param max_retries: Максимальное количество попыток
    :return: True если успешно, False при ошибке
    """
    if not validate_telegram_credentials():
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": int(CHAT_ID),
        "text": text,
        "parse_mode": "HTML"
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети (попытка {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Экспоненциальная задержка
                
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {str(e)}")
            break

    print(f"🔴 Не удалось отправить сообщение после {max_retries} попыток")
    return False
