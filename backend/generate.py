import re
import os
import json
import google.generativeai as genai
from termcolor import colored
from dotenv import load_dotenv
from typing import Tuple, List

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def generate_content(prompt: str, model: str) -> str:
    """
    Generate content using the prompt and model specified.

    Args:
    - prompt: str (the prompt to generate content from)
    - model: str (the model to use for generating content)

    Returns:
    - str (the generated content)
    """
    if model == "gemini":
        model = genai.GenerativeModel("gemini-pro")
        response_raw = model.generate_content(prompt)
        response = response_raw.text
    else:
        raise ValueError("The Model specified is either Invalid or yet to be implemented.")
    
    return response

def generate_content_script(video_core: str, n_stories: int, tts_voice: str, custom_prompt: str) -> str:
    """
    Generate a script for the video using the video core, number of stories, TTS voice and custom prompt specified.

    Args:
    - video_core: str (the video core to use for generating the script)
    - n_stories: int (the number of stories to generate for the script)
    - tts_voice: str (the TTS voice to use for the script)
    - custom_prompt: str (the custom prompt to use for the script)

    Returns:
    - str (the generated script)
    """
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = """
            Generate a script for a video, depending on the subject of the video.

            The script is to be returned as a string with the specified number of paragraphs.

            Here is an example of a string:
            "This is an example string."

            Do not under any circumstance reference this prompt in your response.

            Get straight to the point, don't start with unnecessary things like, "welcome to this video".

            Obviously, the script should be related to the subject of the video.

            YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
            YOU MUST WRITE THE SCRIPT IN THE LANGUAGE SPECIFIED IN [LANGUAGE].
            ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. YOU MUST NOT MENTION THE PROMPT, OR ANYTHING ABOUT THE SCRIPT ITSELF. ALSO, NEVER TALK ABOUT THE AMOUNT OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT.

        """
    
    prompt += f"""
        core: {video_core},
        number of stories: {n_stories},
        TTS voice: {tts_voice}
    """

    response = generate_content(prompt, "gemini")
    print(colored(response, "cyan"))

    if response:
        response = response.replace("*", "")
        response = response.replace("#", "")
        response = re.sub(r"\[.*\]", "", response)
        response = re.sub(r"\(.*\)", "", response)

        stories = response.split("\n\n")
        selected_stories = stories[:n_stories]
        script = "\n\n".join(selected_stories)

        print(colored(f"Stories Used: {len(selected_stories)}", "green"))
        return script

    else:
        print(colored("No response was generated.", "red"))
        return None

def get_search_terms(video_core: str, amount: int, script: str) -> List[str]:
    """
        Generates a JSON file containing the search terms for the video.

        Args:
        - video_core: str (the video core to use for generating the search terms)
        - amount: int (the number of search terms to generate)
        - script: str (the script to use for generating the search terms)

        Returns:
        - List[str] (the search terms)
    """

    prompt = f"""Generate {amount} search terms for stock videos,
    depending on the subject of a video.
    Subject: {video_core}

    The search terms are to be returned as
    a JSON-Array of strings.

    Each search term should consist of 1-3 words,
    always add the main subject of the video.
    
    YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    YOU MUST NOT RETURN ANYTHING ELSE. 
    YOU MUST NOT RETURN THE SCRIPT.
    
    The search terms must be related to the subject of the video.
    Here is an example of a JSON-Array of strings:
    ["search term 1", "search term 2", "search term 3"]

    For context, here is the full text:
    {script}
    """

    response = generate_content(prompt, "gemini")
    print(colored(response, "cyan"))

    search_terms = list()
    
    try:
        search_terms = json.loads(response)
        if not isinstance(search_terms, list) or not all(isinstance(term, str) for term in search_terms):
            raise ValueError("The response is not a JSON-Array of strings.")

    except (json.JSONDecodeError, ValueError):
        response = response[response.find("[") + 1:response.find("]")]
        print(colored("[*] Received weird format: Attempting to clean the data...", "yellow"))

        match = re.search(r'\["(?:[^"\\]|\\.)*"(?:,\s*"[^"\\]*")*\]', response)
        print(match.group())

        if match:
            try:
                search_terms = json.load(match.group())
            except json.JSONDecodeError:
                print(colored("[*] Failed to clean the data.", "red"))
                return []

    print(colored(f"Search Terms Used: {len(search_terms)} and the search terms are: {search_terms}", "green"))
    return search_terms

def meta_data(video_core: str, script: str) -> Tuple[str, str, List[str]]:
    """
    Generates the meta data for the video.

    Args:
    - video_core: str (the video core to use for generating the meta data)
    - script: str (the script to use for generating the meta data)

    Returns:
    - Tuple[str, str, List[str]] (the video title, video description and video tags)
    """

    title_prompt = f"""  
    Generate a catchy and SEO-friendly title for a YouTube shorts video about {video_core}.  
    """  
    title = generate_content(title_prompt, "gemini")

    description_prompt = f"""  
    Write a brief and engaging description for a YouTube shorts video about {video_core}.  
    The video is based on the following script:  
    {script}  
    """  

    description = generate_content(description_prompt, "gemini")

    keywords = get_search_terms(video_core, 6, script)

    return title, description, keywords

if __name__ == '__main__':
    video_core = "Technology"
    n_stories = 3
    tts_voice = "Joanna"
    custom_prompt = ""
    script = generate_content_script(video_core, n_stories, tts_voice, custom_prompt)
    title, description, keywords = meta_data(video_core, script)
    print(colored(f"Title: {title}", "green"))
    print(colored(f"Description: {description}", "green"))
    print(colored(f"Keywords: {keywords}", "green"))