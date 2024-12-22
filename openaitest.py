import os
import google.generativeai as genai
import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini API
genai.configure(api_key="AIzaSyDZ42Qe0HxR0-nD_jMsyZw1PVKFeoAE4PY")  # Using your direct API key
model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to match your working model

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def get_voice_command():
    """Capture and process voice input."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio)
        print(f"User: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, I am unable to reach the internet service.")
        return ""


def generate_gemini_response(prompt):
    """Generate a response using Gemini AI."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error: {e}")
        speak("I was unable to get a response.")
        return None


def jarvis_logic():
    """Main logic for the JARVIS assistant."""
    speak("Hello, how can I help you?")
    while True:
        command = get_voice_command()

        if "hello" in command:
            speak("Hello, there")
        elif "weather" in command:
            speak("Please provide a location")
            location = get_voice_command()
            if location:
                get_weather(location)
        elif "wikipedia" in command:
            speak("What do you want to search on Wikipedia?")
            query = get_voice_command()
            if query:
                wikipedia_search(query)
        elif "open" in command and "google" in command:
            speak("Opening Google Chrome.")
            os.startfile("chrome.exe")
        elif "open" in command and "vs code" in command:
            speak("Opening VS Code.")
            os.startfile("Code.exe")
        elif "open" in command and "youtube" in command:
            speak("Opening YouTube.")
            os.startfile("https://www.youtube.com")
        elif "goodbye" in command or "exit" in command or "bye" in command:
            speak("Goodbye")
            break
        elif command:
            prompt = f"The user said: {command}. Please respond in a helpful way."
            response = generate_gemini_response(prompt)
            if response:
                speak(response)


def get_weather(location):
    """Fetch weather details for a given location."""
    api_key = "YOUR_WEATHER_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}appid={api_key}&q={location}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request is not successful
        weather_data = response.json()
        if weather_data["cod"] != "404":
            main_data = weather_data["main"]
            temp_kelvin = main_data["temp"]
            temp_celsius = temp_kelvin - 273.15
            humidity = main_data["humidity"]
            description = weather_data["weather"][0]["description"]
            speak(
                f"The temperature in {location} is {temp_celsius:.2f} degrees Celsius, "
                f"with a humidity of {humidity} percent. The weather is {description}."
            )
        else:
            speak("Could not find weather for that location.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        speak("There was a problem getting the weather info.")


def wikipedia_search(query):
    """Search Wikipedia for a summary of the query."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        extract = data.get("extract", "Could not find information for the query.")
        speak(extract)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        speak("Unable to connect to Wikipedia service.")


if __name__ == "__main__":
    jarvis_logic()
