
import time
import schedule
from run_pipeline import run_auto_trending_pipeline

def job():
    print("📅 Расписание: Запуск авто-тренд пайплайна")
    run_auto_trending_pipeline()

# Запускаем каждый день в 00:00, 06:00, 12:00, 18:00
schedule.every().day.at("00:00").do(job)
schedule.every().day.at("06:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("18:00").do(job)

print("✅ Расписание активировано. Ожидаем время запуска...")

while True:
    schedule.run_pending()
    time.sleep(60)
