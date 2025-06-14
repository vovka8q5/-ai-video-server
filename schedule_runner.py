import schedule
import time
import subprocess
from notifier import send_message
from datetime import datetime, timezone

SCHEDULE_TIMES = ["21:03"]  # Тестовое время
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

def run_pipeline_job():
    try:
        print(f"\n🔴 [{datetime.now(timezone.utc)}] Запуск пайплайна...")
        send_message("🔄 Начало обработки видео")
        
        result = subprocess.run(
            PIPELINE_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1800,
            check=True
        )
        
        print(f"✅ Вывод пайплайна:\n{result.stdout.decode()}")
        send_message("✅ Видео успешно обработано")
        
    except subprocess.TimeoutExpired:
        error_msg = "❌ Пайплайн превысил 30-минутный лимит"
        print(error_msg)
        send_message(error_msg)
    except Exception as e:
        error_msg = f"🔥 Ошибка: {str(e)}"
        print(error_msg)
        send_message(error_msg)

def main():
    print(f"⏰ Серверное время UTC: {datetime.now(timezone.utc)}")
    send_message("🚀 Планировщик активирован")
    
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)
        print(f"⏳ Запланирован запуск на {time_str} UTC")

    while True:
        try:
            schedule.run_pending()
            time.sleep(10)
        except Exception as e:
            print(f"🛑 Ошибка в основном цикле: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
