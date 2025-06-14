from notifier import send_message
from download_video import download_from_youtube
from preprocess_video import convert_to_shorts_format
from stylize_video import apply_ai_style
from subtitle_generator import generate_subtitles
from upload_youtube import upload_to_youtube
import os

def run_pipeline():
    try:
        send_message("🎬 Начинаем обработку видео")
        print("🎬 Запуск пайплайна...")

        # 1. Получаем URL видео
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Пример, лучше брать из fetch_trending.py
        
        # 2. Скачиваем
        raw_video = download_from_youtube(video_url)
        
        # 3. Конвертируем в Shorts
        shorts_video = convert_to_shorts_format(raw_video)
        
        # 4. Стилизуем
        stylized_video = apply_ai_style(shorts_video)
        
        # 5. Генерируем субтитры
        generate_subtitles(stylized_video)
        
        # 6. Загружаем на YouTube
        upload_to_youtube(stylized_video)
        
        print("✅ Обработка завершена")
        send_message("✅ Видео загружено и опубликовано")
    
    except Exception as e:
        print(f"❌ Ошибка в пайплайне: {str(e)}")
        send_message(f"❌ Ошибка в пайплайне: {str(e)}")

if __name__ == "__main__":
    run_pipeline()
