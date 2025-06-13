# schedule_runner.py

import schedule
import time
import subprocess

def job():
    print("🚀 Старт задачи: run_pipeline.py")
    subprocess.run(["python", "run_pipeline.py"])

# Расписание: 4 раза в сутки (UTC)
schedule.every().day.at("00:00").do(job)
schedule.every().day.at("06:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("18:00").do(job)

print("⏳ Ожидание времени запуска...")

while True:
    schedule.run_pending()
    time.sleep(30)
