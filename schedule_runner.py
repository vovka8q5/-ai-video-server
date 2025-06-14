import time
import subprocess
from datetime import datetime, timezone
from notifier import send_message

SCHEDULE = ["19:55"]  # Формат: "HH:MM"
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def get_current_time():
    return datetime.now(timezone.utc).strftime("%H:%M")

def main():
    print("📡 Планировщик активирован...")
    try:
        send_message("📡 Планировщик запущен на сервере!")
    except Exception as e:
        print(f"⚠️ Не удалось отправить уведомление о запуске: {e}")

    already_ran = set()

    while True:
        current_time = get_current_time()
        print(f"🕒 Текущее время UTC: {current_time}")

        if current_time in SCHEDULE and current_time not in already_ran:
            print(f"🚀 Запуск run_pipeline.py в {current_time}")
            try:
                send_message(f"🚀 Старт обработки видео в {current_time}")
            except Exception as e:
                print(f"⚠️ Не удалось отправить уведомление о старте: {e}")

            try:
                subprocess.run(PIPELINE_COMMAND, check=True)
                already_ran.add(current_time)
            except subprocess.CalledProcessError as e:
                print(f"❌ Ошибка при запуске pipeline: {e}")
                try:
                    send_message(f"❌ Ошибка при запуске pipeline: {e}")
                except Exception as tg_err:
                    print(f"⚠️ Не удалось отправить уведомление об ошибке: {tg_err}")

        # Сброс на следующий день
        if datetime.now(timezone.utc).hour == 0 and datetime.now(timezone.utc).minute == 0:
            already_ran.clear()

        time.sleep(30)

if __name__ == "__main__":
    main()
