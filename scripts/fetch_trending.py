def get_trending_video_urls(count=3):
    import requests
    from bs4 import BeautifulSoup

    print("📡 Получаем тренды YouTube...")
    try:
        trending_url = "https://www.youtube.com/feed/trending"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(trending_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("❌ Ошибка получения трендов:", e)
        return []

    urls = []
    for link in soup.select("a[href^='/watch']"):
        video_id = link.get("href").split("v=")[-1]
        full_url = f"https://www.youtube.com{link.get('href')}"
        if full_url not in urls:
            urls.append(full_url)
        if len(urls) >= count:
            break
    print("✅ Тренды:", urls)
    return urls
