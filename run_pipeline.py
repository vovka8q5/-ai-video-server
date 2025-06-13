# run_pipeline.py

from scripts.fetch_trending import get_trending_video_urls
from scripts.download_video import download_from_youtube
from scripts.preprocess_video import convert_to_shorts_format
from scripts.stylize_video import apply_ai_style
from scripts.subtitle_generator import generate_subtitles
from uploader.upload_youtube import upload_to_youtube

def run_full_pipeline(video_url: str, style: str = "anime"):
    print(f"🚀 Загружаем видео: {video_url}")
    video_path = download_from_youtube(video_url)
    print(f"📼 Скачано: {video_path}")

    short_path = convert_to_shorts_format(video_path)
    print(f"✂️ Отформатировано: {short_path}")

    stylized_path = apply_ai_style(short_path, style)
    print(f"🎨 Стилизация готова: {stylized_path}")

    generate_subtitles(stylized_path)
    print("💬 Субтитры добавлены")

    upload_to_youtube(stylized_path)
    print("☁️ Загрузка завершена")

def run_auto_trending_pipeline():
    print("📡 Запуск авто-тренд пайплайна...")
    urls = get_trending_video_urls(count=1)
    print(f"✅ Тренды: {urls}")
    for url in urls:
        run_full_pipeline(url, style="anime")
    print("✅ Все видео обработаны")

if __name__ == "__main__":
    run_auto_trending_pipeline()
