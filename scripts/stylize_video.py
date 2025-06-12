def apply_ai_style(input_path: str, style: str = "anime", output_path="stylized/stylized.mp4") -> str:
    import shutil
    shutil.copy(input_path, output_path)  # временно без реальной нейросети
    return output_path
