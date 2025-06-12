def convert_to_shorts_format(input_path: str, output_path="output/shorts_ready/short.mp4") -> str:
    import subprocess
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", "scale=720:1280,setsar=1", "-t", "00:00:59",
        "-y", output_path
    ]
    subprocess.run(cmd)
    return output_path
