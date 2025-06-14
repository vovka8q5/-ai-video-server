# schedule_runner.py (тестовая версия)
import schedule
import time
import subprocess
from notifier import send_message
from datetime import datetime, timezone

# ТЕСТОВОЕ РАСПИСАНИЕ (только 00:00 UTC)
SCHEDULE_TIMES = ["20:46"]  # Только одно время для теста
# SCHEDULE_TIMES = ["00:00", "06:00", "12:00", "18:00"]  # Оригинальное расписание (закомментировано)

PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def run_pipeline_job():
    current_time = datetime.now(timezone.utc).strftime("%H:%M")
    print(f"⏰ Тестовый запуск пайплайна в {current_time} UTC")
    
    try:
        send_message(f"🧪 Тестовый запуск в {current_time} UTC")
        
        # Для теста можно добавить принудительную задержку
        print("🔄 Имитация обработки видео (10 сек)...")
        time.sleep(10)
        
        result = subprocess.run(
            PIPELINE_COMMAND,
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            send_message("✅ Тест успешен! Пайплайн работает")
        else:
            error_msg = result.stderr[:500]
            send_message(f"❌ Тест не пройден:\n{error_msg}")

    except Exception as e:
        send_message(f"🔥 Тестовая ошибка: {str(e)}")

def main():
    send_message("🔧 Начат тестовый режим планировщика")
    
    # Для теста можно добавить принудительный запуск
    if datetime.now(timezone.utc).hour == 23:  # Если сейчас 23:00 UTC
        print("🛠 Принудительный тестовый запуск")
        run_pipeline_job()
    
    # Настройка расписания
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)
        print(f"⏳ Тестовая задача на {time_str} UTC")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
