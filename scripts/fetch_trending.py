def get_trending_video_urls(count=3):
    import requests

    print("📡 Получаем тренды YouTube через API...")

    API_KEY = ""
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet&chart=mostPopular&regionCode=US&maxResults={count}&key={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        urls = []
        for item in data.get("items", []):
            video_id = item["id"]
            full_url = f"https://www.youtube.com/watch?v={video_id}"
            urls.append(full_url)

        print("✅ Тренды:", urls)
        return urls
    except Exception as e:
        print("❌ Ошибка при запросе API:", e)
        return []
