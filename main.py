import moviepy.editor as mpy
from moviepy.video.tools.segmenting import findObjects
from modules.text_gen import text_generation

import os
from dotenv import load_dotenv
load_dotenv()

import pyttsx3 as tts

engine = tts.init()


White = (255, 255, 255)
ScreenSize = (720, 460)
VerticalMargin = 30
HorizontalMargin = 100

Logo_Path = "Logo.png"

sblogo = mpy.ImageClip(Logo_Path).\
    set_position(('center', 0)).\
        resize(width=200)


def text_to_audio(text: str, *voice: str):
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.save_to_file(text, "audio.mp3")
    engine.runAndWait()
    return "audio.mp3"

def text_to_video(text: str, water_mark: str):

    txt_clip = mpy.TextClip(
            text,
            font="Charter-bold",
            color="RoyalBlue4",
            kerning=4,
            fontsize=30,
        ).set_position(("center", sblogo.size[1] + VerticalMargin))

    txt_watermark = mpy.TextClip(
        water_mark,
        color="#ff8c82",
        kerning=4,
        fontsize=22,
        stroke_color="#ff8c82",
        stroke_width=0.4,
    ).set_position(("center", sblogo.size[1] + txt_clip.size[1] + VerticalMargin * 6))

    txt_image = mpy.ImageClip("./Logo.png").set_duration(5).resize(width=ScreenSize[0])
    
    final = mpy.CompositeVideoClip([sblogo, txt_clip,txt_image, txt_watermark], size=ScreenSize).set_duration(10)

    audio_clip = mpy.AudioFileClip("audio.mp3")
    txt_audio = mpy.CompositeAudioClip([audio_clip])

    final = final.set_audio(txt_audio)
    final.write_videofile("output.mp4", fps=24, codec="libx264")


def main():
    text = text_generation("Write a Aesthetic General Knowledge")
    text_to_audio(text=text)
    text_to_video(text=text, water_mark="Watermark")

if __name__ == "__main__":
    main()
