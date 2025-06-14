# run_pipeline.py

from scripts.fetch_trending import get_trending_video_urls
from scripts.download_video import download_from_youtube
from scripts.preprocess_video import convert_to_shorts_format
from scripts.stylize_video import apply_ai_style
from scripts.subtitle_generator import generate_subtitles
from uploader.upload_youtube import upload_to_youtube
from notifier import send_message


def run_full_pipeline(video_url: str, style: str = "anime"):
    try:
        send_message(f"🎬 Старт обработки: {video_url}")

        video_path = download_from_youtube(video_url)
        short_path = convert_to_shorts_format(video_path)
        stylized_path = apply_ai_style(short_path, style)
        generate_subtitles(stylized_path)
        upload_to_youtube(stylized_path)

        send_message(f"✅ Видео успешно загружено: {video_url}")
    except Exception as e:
        send_message(f"❌ Ошибка при обработке видео:\n{str(e)}")
        print(f"❌ Ошибка: {e}")


def run_auto_trending_pipeline():
    send_message("📡 Запуск авто-тренд пайплайна...")

    urls = get_trending_video_urls(count=1)
    if not urls:
        send_message("⚠️ Тренды не найдены.")
        return

    send_message(f"🔗 Найдено видео: {urls[0]}")
    for url in urls:
        run_full_pipeline(url, style="anime")

    send_message("🏁 Обработка завершена.")


if __name__ == "__main__":
    run_auto_trending_pipeline()
