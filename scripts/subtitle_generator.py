import os
import subprocess
import whisper

def extract_audio(video_path: str, audio_path="output/audio.wav"):
    subprocess.run(["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1", "-y", audio_path])
    return audio_path

def generate_subtitles(video_path: str, lang="en") -> dict:
    model = whisper.load_model("base")
    audio_path = extract_audio(video_path)
    result = model.transcribe(audio_path, language=lang)

    srt_path = video_path.replace(".mp4", ".srt")
    txt_path = video_path.replace(".mp4", ".txt")

    with open(txt_path, "w") as f:
        f.write(result["text"])
    with open(srt_path, "w") as f:
        f.write("1\\n00:00:00,000 --> 00:00:59,000\\n" + result["text"] + "\\n")

    return {"text": txt_path, "srt": srt_path}
