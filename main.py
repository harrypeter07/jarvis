import os
import webbrowser

import speech_recognition as sr
import win32com.client
import openai

#pending: open instagram and login using -WEBDRIVER,,,RESEARCH IN THIS TOOL


# Initialize the speaker
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        r.adjust_for_ambient_noise(source)  # Optional: adjusts for background noise
        print("Listening...")
        try:
            audio = r.listen(source)  # Capture the audio
            query = r.recognize_google(audio, language="en-IN")  # Use Google's API for recognition
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Google API error: {e}")
            return ""

while True:
    print("Listening...")
    text = takeCommand()

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.org"],  # Corrected URL for Wikipedia
        ["google", "https://www.google.com"],
        ["github", "https://www.github.com"],
        ["reddit", "https://www.reddit.com"],
        ["stack overflow", "https://stackoverflow.com"],
        ["twitter", "https://www.twitter.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["amazon", "https://www.amazon.com"],
        ["facebook", "https://www.facebook.com"],
        ["quora", "https://www.quora.com"]
    ]
    speaker.Speak(f"{text}")
    for site in sites:
        if f"Open {site[0]}".lower() in text.lower():
            speaker.Speak(f"opening {site[0]} sir...")
            webbrowser.open(site[1])


    # if "open music" in text:
    #     musicpath = "C:/Users/ASUS/Downloads/hindi_speech.mp3"
    #     os.startfile(musicpath)