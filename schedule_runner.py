# schedule_runner.py

import time
import subprocess
from datetime import datetime, timezone

# 🕓 Времена запуска в формате UTC (24 часа)
SCHEDULED_TIMES = ["00:00", "06:00", "12:00", "18:00"]

def log(message: str):
    """Печатает сообщение с меткой времени в UTC"""
    timestamp = datetime.now(timezone.utc).strftime("[%Y-%m-%d %H:%M:%S UTC]")
    print(f"{timestamp} {message}")

def run_pipeline():
    log("🚀 Запускаем run_pipeline.py...")
    try:
        result = subprocess.run(["python", "run_pipeline.py"], capture_output=True, text=True)
        if result.returncode == 0:
            log("✅ Успешно завершено.")
        else:
            log(f"❌ Ошибка! Код завершения: {result.returncode}")
            log(f"🪵 STDOUT:\n{result.stdout}")
            log(f"🪵 STDERR:\n{result.stderr}")
    except Exception as e:
        log(f"💥 Исключение при запуске пайплайна: {str(e)}")

def main():
    log("🟢 Сервис запущен. Ожидаем расписание...")
    already_ran = set()

    while True:
        now_utc = datetime.now(timezone.utc)
        current_time = now_utc.strftime("%H:%M")

        if current_time in SCHEDULED_TIMES and current_time not in already_ran:
            log(f"🕒 Время совпало с {current_time}. Запускаем видео-процесс.")
            run_pipeline()
            already_ran.add(current_time)

            if len(already_ran) == len(SCHEDULED_TIMES):
                log("📦 Все запланированные запуска за день выполнены.")

        if current_time == "00:01":
            already_ran.clear()
            log("🔁 Новый день. Сброс флага запусков.")

        time.sleep(60)  # Проверяем каждую минуту

if __name__ == "__main__":
    main()
