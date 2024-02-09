import moviepy.editor as mpy
from moviepy.video.tools.segmenting import findObjects
from modules.text_gen import text_generation
from modules.video_gen import generate_video
from modules.audio_gen import generate_audio

import os
from dotenv import load_dotenv
load_dotenv()

White = (255, 255, 255)
ScreenSize = (720, 460)
VerticalMargin = 30
HorizontalMargin = 100

def main():
    text = text_generation("Write a Aesthetic General Knowledge")
    generate_audio(text=text)
    generate_video(text=text, water_mark="Watermark")

if __name__ == "__main__":
    main()
