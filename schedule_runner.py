import schedule
import time
from notifier import send_message
from datetime import datetime, timezone

# Конфигурация расписания (UTC время)
SCHEDULE_TIMES = ["20:40"]  # 4 раза в сутки ["00:00", "06:00", "12:00", "18:00"]
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def run_pipeline_job():
    try:
        current_time = datetime.now(timezone.utc).strftime("%H:%M")
        send_message(f"⏰ Запуск пайплайна в {current_time} UTC")
        
        result = subprocess.run(
            PIPELINE_COMMAND,
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            send_message("✅ Пайплайн успешно завершен")
        else:
            send_message(f"❌ Ошибка пайплайна (код {result.returncode}):\n{result.stderr[:1000]}")

    except Exception as e:
        send_message(f"🔥 Критическая ошибка: {str(e)}")

def main():
    send_message("🚀 Планировщик видео запущен")
    
    # Настройка расписания
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)

    # Основной цикл
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
