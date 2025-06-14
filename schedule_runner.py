# schedule_runner.py
import time
import subprocess
from datetime import datetime
from notifier import send_message

# ⏰ Время запуска в формате UTC
SCHEDULE = ["00:00", "06:00", "12:00", "18:00"]
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def get_current_time():
    return datetime.utcnow().strftime("%H:%M")

def main():
    print("📡 Планировщик активирован...")
    send_message("📡 Планировщик запущен на сервере!")
    already_ran = set()

    while True:
        current_time = get_current_time()
        print(f"🕒 Текущее время UTC: {current_time}")

        if current_time in SCHEDULE and current_time not in already_ran:
            print(f"🚀 Запуск run_pipeline.py в {current_time}")
            send_message(f"🚀 Старт обработки видео в {current_time}")
            subprocess.run(PIPELINE_COMMAND)
            already_ran.add(current_time)

        if len(already_ran) == len(SCHEDULE):
            print("🔄 Сброс расписания")
            already_ran.clear()

        time.sleep(30)

if __name__ == "__main__":
    main()
