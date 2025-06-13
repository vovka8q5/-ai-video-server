# schedule_runner.py — Планировщик запуска run_pipeline.py без Render Cron

import time
import subprocess
from datetime import datetime

# ⏰ Расписание запусков (UTC)
SCHEDULE = ["00:00", "06:00", "12:00", "18:00"]

# 📁 Путь до пайплайна
PIPELINE_COMMAND = ["python", "run_pipeline.py"]


def should_run_now():
    now = datetime.utcnow().strftime("%H:%M")
    return now in SCHEDULE


def main():
    print("📡 Автозапуск планировщика активирован...\n")
    already_ran = set()

    while True:
        current_time = datetime.utcnow().strftime("%H:%M")

        if current_time in SCHEDULE and current_time not in already_ran:
            print(f"🚀 {current_time} — запуск run_pipeline.py")
            subprocess.run(PIPELINE_COMMAND)
            already_ran.add(current_time)

        # Ежедневный сброс
        if len(already_ran) == len(SCHEDULE):
            print("🔄 Сброс расписания на следующий день")
            already_ran.clear()

        time.sleep(30)  # Проверять каждые 30 секунд


if __name__ == "__main__":
    main()
