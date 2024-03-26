import pathlib
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import pyttsx3 as tts
load_dotenv()
BARD_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=BARD_API_KEY)

def eleven_speak(text, file_name):

    '''Speaks'''

    engine = tts.init()
    engine.setProperty('rate', 200)
    path = 'audio'
    if os.path.exists(path):
        engine.save_to_file(text, f'audio/{file_name}.mp3')
        engine.runAndWait()
    else:
        os.mkdir(path)
        engine.save_to_file(text, f'audio/{file_name}.mp3')
        engine.runAndWait()

def generate_script(prompt, stories):
    model = genai.GenerativeModel('gemini-pro')
    default_prompt = """from now on return the output as regular text and the story should look
                    like it being narrated by someone. Write a Short and simple story,
                    You have to write maximum 170 words I want a plain text no symbols just the script, 
                    also the script content must be in 50 seconds duration, dont include any symbols or special characters,"""
    title_prompt = "For this story, I want you to write a 3 to 5 words title"

    for i in range(stories):
        story = model.generate_content(f"{default_prompt},{prompt}")
        title = model.generate_content(f"{title_prompt},{story}")
        
        print(f"Title: {title.text}")
        print(f"Story: {story.text}")

        json_data = json.dumps({"title": title.text, "story": story.text})
        story_path = "story"

        if not os.path.exists(story_path):
            os.mkdir(story_path)
            print(f"Story directory created at {story_path}")
        with open(f"{story_path}/story_{i}.json", "w") as f:
            f.write(json_data)