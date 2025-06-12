from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle
from scripts.gpt_title_generator import generate_youtube_title_description

def upload_to_youtube(video_path: str):
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)
    meta = generate_youtube_title_description("аниме-стиль популярного видео")

    request_body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"].replace("#", "").split(),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/*", resumable=True)
    youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()
