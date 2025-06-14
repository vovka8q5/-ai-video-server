import schedule
import time
import subprocess
import threading
from notifier import send_message
from datetime import datetime, timezone

SCHEDULE_TIMES = ["21:08"]  # Тестовое время (UTC)
PIPELINE_COMMAND = ["python", "run_pipeline.py"]

# Глобальный флаг для контроля работы
is_running = True

def run_pipeline_job():
    """Запускает пайплайн в отдельном потоке"""
    def worker():
        try:
            current_time = datetime.now(timezone.utc).strftime("%H:%M:%S")
            print(f"\n🔴 [{current_time}] Старт пайплайна...")
            send_message(f"⏳ Начало обработки видео в {current_time} UTC")
            
            # Запуск с таймаутом 30 минут
            result = subprocess.run(
                PIPELINE_COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1800,
                check=True,
                text=True
            )
            
            print(f"✅ Успешно завершено:\n{result.stdout}")
            send_message(f"✅ Видео обработано в {datetime.now(timezone.utc).strftime('%H:%M:%S')} UTC")
            
        except subprocess.TimeoutExpired:
            error_msg = "❌ Пайплайн завис (таймаут 30 мин)"
            print(error_msg)
            send_message(error_msg)
        except Exception as e:
            error_msg = f"🔥 Ошибка: {str(e)}"
            print(error_msg)
            send_message(error_msg)

    # Запуск в отдельном потоке
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

def main():
    print(f"⏰ Сервер запущен (UTC: {datetime.now(timezone.utc).strftime('%H:%M:%S')})")
    send_message("🚀 Планировщик активирован")
    
    # Настройка расписания
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(run_pipeline_job)
        print(f"⏳ Расписание: ежедневно в {time_str} UTC")

    # Основной цикл с обработкой прерываний
    try:
        while is_running:
            schedule.run_pending()
            time.sleep(10)  # Проверка каждые 10 сек
            print(f"🔄 Активен (UTC: {datetime.now(timezone.utc).strftime('%H:%M:%S')})", end='\r')
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервиса...")
    finally:
        send_message("🔴 Планировщик остановлен")

if __name__ == "__main__":
    main()
