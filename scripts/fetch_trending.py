def get_trending_video_urls(count=3):
    import requests
    from bs4 import BeautifulSoup

    trending_url = "https://www.youtube.com/feed/trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(trending_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = []
    for link in soup.select("a[href^='/watch']"):
        full_url = f"https://www.youtube.com{link.get('href')}"
        if full_url not in urls:
            urls.append(full_url)
        if len(urls) >= count:
            break
    return urls
