from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import CompositeAudioClip, concatenate_audioclips
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, ImageClip, CompositeVideoClip, AudioFileClip
import json, os
import whisper
from modules.text_gen import generate_script, eleven_speak

def speech_to_text(audio_file):
    model = whisper.load_model("base")
    data = model.transcribe(audio_file, word_timestamps=True)

    start = [data['segments'][i]['words'][j]['start'] for i in range(len(data['segments'])) for j in range(len(data['segments'][i]['words']))]
    end = [data['segments'][i]['words'][j]['end'] for i in range(len(data['segments'])) for j in range(len(data['segments'][i]['words']))]
    text = [data['segments'][i]['words'][j]['word'] for i in range(len(data['segments'])) for j in range(len(data['segments'][i]['words']))]

    return [start, end, text]

def generate_video(video_title: str, number_of_videos: int):
    generate_script(video_title, number_of_videos)
    
    for i in range(number_of_videos):
        print(i)

        story_path = "story"
        with open(f'{story_path}/story_{i}.json', 'r') as f:
            text = json.load(f)
            text = text['story']
            text = [word.replace('\n', '') for word in text]
            new_text = ''.join(text)
            print(new_text)
            eleven_speak(new_text, f'story_{i}')

        with open(f'{story_path}/story_{i}.json', 'r') as file:
            print(f'Generating video for story {i}')
            text = json.load(file)
            text = text['story']
        
        words = text.split(' ')

        generator = lambda txt: TextClip(txt, 
                                    fontsize=70, 
                                    color='white', 
                                    bg_color='none', 
                                    font='Arial-Bold',
                                    method = 'caption',
                                    size = (1920, 1080))

        # def clip_generator():
        #     for _ in words:
        #         yield CompositeVideoClip([ImageClip('Z_1.jpg').set_duration(0.5).set_position('center')], size=(720, 1280))

        # clips = concatenate_videoclips(clip_generator(), method="compose")

        speech = speech_to_text(f'audio/story_{i}.mp3')
        print(f'Accessing speech for story {i}')
        subs = [((speech[0][k], speech[1][k]), speech[2][k]) for k in range(len(speech[0]))]

        subtitles = SubtitlesClip(subs, generator)
        audio_clip = AudioFileClip(f'audio/story_{i}.mp3')
        video = VideoFileClip('./assets/BG.mp4')
        final_complete = CompositeVideoClip([video.set_duration(audio_clip.duration), subtitles.set_position(('center', 'center'))])
        final_complete = final_complete.set_audio(audio_clip)
        final_complete.write_videofile(f"output_{i}.mp4" , fps=24, bitrate = '8000k', preset = 'fast', codec = 'libx264')
        final_complete.close()