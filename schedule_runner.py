import time
import subprocess
import datetime

# Время в формате UTC — расписание загрузок
SCHEDULED_TIMES = ["00:00", "06:00", "12:00", "18:00"]

LOG_FILE = "schedule_log.txt"

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"⚠️ Ошибка записи в лог: {e}")

def current_time_utc():
    return datetime.datetime.utcnow().strftime("%H:%M")

def run_pipeline():
    log("🚀 Запуск run_pipeline.py")
    try:
        result = subprocess.run(["python", "run_pipeline.py"],
                                capture_output=True, text=True, timeout=1800)
        log("✅ STDOUT:\n" + result.stdout)
        log("⚠️ STDERR:\n" + result.stderr)
    except subprocess.TimeoutExpired:
        log("❌ Таймаут выполнения run_pipeline.py")

if __name__ == "__main__":
    log("🟢 schedule_runner запущен и ожидает расписание...")
    already_ran = set()

    while True:
        now = current_time_utc()

        if now in SCHEDULED_TIMES and now not in already_ran:
            log(f"⏰ Время по расписанию: {now}")
            run_pipeline()
            already_ran.add(now)

        # Очистка уже выполненных запусков на следующий день
        if now == "00:01":
            already_ran.clear()
            log("🔁 Очистка списка уже выполненных времён")

        time.sleep(10)  # Проверять каждые 10 секунд
