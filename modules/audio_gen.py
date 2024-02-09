import pyttsx3 as tts # will change it to something cooler

def generate_audio(text: str):
    engine = tts.init()
    engine.save_to_file(text, 'sample.mp3')
    engine.runAndWait()