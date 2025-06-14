# schedule_runner.py

import subprocess
import time
from datetime import datetime, timezone

# Время запуска (UTC): каждый день в 00:00, 06:00, 12:00, 18:00
SCHEDULED_TIMES = ["00:00", "06:00", "12:00", "18:00"]

# Логи
LOG_PREFIX = "[SCHEDULER]"

def log(message):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"{LOG_PREFIX} {now} - {message}")

# Проверка, совпадает ли время
def is_scheduled_time():
    current_time = datetime.now(timezone.utc).strftime("%H:%M")
    return current_time in SCHEDULED_TIMES

def run_pipeline():
    log("Запуск run_pipeline.py...")
    try:
        result = subprocess.run(["python", "run_pipeline.py"], capture_output=True, text=True, timeout=600)
        log("Выполнено run_pipeline.py")
        log(f"[OUTPUT]:\n{result.stdout}")
        if result.stderr:
            log(f"[ERROR]:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        log("❌ Ошибка: run_pipeline.py превысил лимит времени")
    except Exception as e:
        log(f"❌ Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    log("Запуск планировщика...")
    while True:
        try:
            if is_scheduled_time():
                log("✅ Время совпадает с расписанием. Запуск...")
                run_pipeline()
                log("🕒 Засыпаем на 60 секунд, чтобы избежать повторного запуска...")
                time.sleep(60)
            else:
                log("⏳ Пока не время. Ждём 15 секунд...")
                time.sleep(15)
        except KeyboardInterrupt:
            log("⛔ Остановка по запросу пользователя")
            break
        except Exception as e:
            log(f"❌ Ошибка в основном цикле: {e}")
