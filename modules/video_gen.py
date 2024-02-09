from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *

def generate_video(speech: list):
    with open('samp.txt', 'r') as file:
        text = file.read()
    
    lst = text.split(' ')

    clips = []

    generator = lambda txt: TextClip(txt, 
                                fontsize=70, 
                                color='white', 
                                bg_color='none', 
                                font='Arial-Bold',
                                method = 'caption',
                                size = (1920, 1080))

    clips = [CompositeVideoClip([ImageClip('Z_1.jpg').set_duration(0.5).set_position('center')], size=(1920, 1080)) for _ in lst]

    subs = [((speech[0][k], speech[1][k]), speech[2][k]) for k in range(len(speech[0]))]
        

    subtitles = SubtitlesClip(subs, generator)

    final = concatenate_videoclips(clips)
    audio = AudioFileClip("samp.mp3")
    final = final.set_audio(audio)
    final_complete = CompositeVideoClip([final, subtitles.set_position(('center', 'bottom'))])
    final_complete.write_videofile("output0.mp4", fps=24, codec = 'libx264')