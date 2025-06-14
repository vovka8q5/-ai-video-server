import schedule
import time
import subprocess
from notifier import send_message
from datetime import datetime, timezone

SCHEDULE_TIMES = ["20:06"]  # Тестовое время, потом замените на ["00:00", "06:00", "12:00", "18:00"]
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def run_pipeline_job():
    current_time = datetime.now(timezone.utc).strftime("%H:%M")
    print(f"🚀 Запуск пайплайна в {current_time} UTC")
    try:
        send_message(f"🚀 Старт обработки видео в {current_time} UTC")
        subprocess.run(PIPELINE_COMMAND, check=True)
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        send_message(f"❌ Ошибка пайплайна: {str(e)}")

def main():
    print("📡 Планировщик активирован...")
    send_message("📡 Планировщик запущен на сервере!")

    # Настраиваем расписание
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту

if __name__ == "__main__":
    main()
