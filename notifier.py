import os
import requests
from typing import Optional
from datetime import datetime

# Загрузка переменных окружения
BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

def validate_telegram_credentials() -> bool:
    """Проверяет валидность учетных данных Telegram"""
    if not BOT_TOKEN or not BOT_TOKEN.startswith('bot'):
        print("❌ Invalid Telegram Bot Token. Must start with 'bot'")
        return False
    
    if not CHAT_ID or not CHAT_ID.strip().isdigit():
        print("❌ Invalid Chat ID. Must be a numeric value")
        return False
    
    return True

def send_message(text: str, max_retries: int = 3) -> bool:
    """
    Отправляет сообщение в Telegram чат
    :param text: Текст сообщения
    :param max_retries: Максимальное количество попыток отправки
    :return: True если отправлено успешно, False в случае ошибки
    """
    if not validate_telegram_credentials():
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": int(CHAT_ID),
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=10,
                headers={"User-Agent": "AI Video Server"}
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("ok"):
                error_msg = data.get("description", "Unknown error")
                print(f"❌ Telegram API error (attempt {attempt + 1}): {error_msg}")
                if "retry_after" in data:
                    time.sleep(data["retry_after"])
                continue

            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        except Exception as e:
            print(f"❌ Unexpected error (attempt {attempt + 1}): {str(e)}")
            break

    # Если все попытки неудачны, логируем последнюю ошибку
    last_error = {
        "timestamp": datetime.now().isoformat(),
        "bot_token": BOT_TOKEN[:4] + "..." + BOT_TOKEN[-4:] if BOT_TOKEN else None,
        "chat_id": CHAT_ID,
        "error": str(e),
        "message": text[:100] + "..." if len(text) > 100 else text
    }
    print(f"🔴 Failed to send message after {max_retries} attempts. Details: {last_error}")
    return False

def send_message_with_logging(text: str) -> bool:
    """Отправляет сообщение с дополнительным логированием"""
    success = send_message(text)
    if success:
        print(f"✅ Message sent to Telegram at {datetime.now()}")
    return success

# Пример использования (для тестов)
if __name__ == "__main__":
    test_message = "🔴 Тестовое сообщение от сервера\n" \
                   f"Время: {datetime.now()}\n" \
                   "Это проверка работы бота"
    
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Тестовый режим: переменные окружения не заданы")
        test_result = send_message(test_message)
    else:
        test_result = send_message_with_logging(test_message)
    
    print(f"Результат отправки: {'Успешно' if test_result else 'Ошибка'}")
