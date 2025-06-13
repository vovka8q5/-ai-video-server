import os


os.makedirs("input/raw_videos", exist_ok=True)
os.makedirs("output/shorts_ready", exist_ok=True)
os.makedirs("stylized", exist_ok=True)

from scripts.download_video import download_from_youtube
from scripts.preprocess_video import convert_to_shorts_format
from scripts.stylize_video import apply_ai_style
from scripts.subtitle_generator import generate_subtitles
from uploader.upload_youtube import upload_to_youtube
from scripts.fetch_trending import get_trending_video_urls

def run_full_pipeline(video_url: str, style: str = "anime"):
    video_path = download_from_youtube(video_url)
    short_path = convert_to_shorts_format(video_path)
    stylized_path = apply_ai_style(short_path, style)
    generate_subtitles(stylized_path)
    upload_to_youtube(stylized_path)

def run_auto_trending_pipeline():
    urls = get_trending_video_urls(count=3)
    for url in urls:
        run_full_pipeline(url)

if __name__ == "__main__":
    run_auto_trending_pipeline()
