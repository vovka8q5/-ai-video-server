import subprocess
import sys
from datetime import datetime, timezone
import schedule
import time

SCHEDULE_TIMES = ["21:16"]  # UTC время
PIPELINE_COMMAND = [sys.executable, "run_pipeline.py"]  # Используем тот же Python

def log(message):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")
    with open("scheduler.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_pipeline_job():
    log("🔴 Запуск пайплайна...")
    try:
        result = subprocess.run(
            PIPELINE_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=1800
        )
        log(f"✅ Завершён с кодом {result.returncode}")
        log(f"STDOUT: {result.stdout[:200]}...")
        log(f"STDERR: {result.stderr[:200]}...")
    except subprocess.TimeoutExpired:
        log("❌ Таймаут 30 минут превышен")
    except Exception as e:
        log(f"🔥 Ошибка: {str(e)}")

def main():
    log(f"⏰ Сервис запущен (Python {sys.version})")
    
    # Тестовый запуск сразу
    log("🧪 Тестовый запуск пайплайна...")
    run_pipeline_job()
    
    # Настройка расписания
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)
        log(f"⏳ Запланировано на {time_str} UTC")

    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    main()
