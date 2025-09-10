import os
import datetime
import webbrowser
import pyttsx3
import requests
import speech_recognition as sr
import musicLibrary  # your custom music library
from google.cloud import speech

# ------------------ Setup ------------------
# Set path to your Google Cloud service account JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/google_key.json"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------ Google Cloud Speech ------------------
def recognize_speech_google_cloud(audio_data):
    """Convert audio data from microphone to text using Google Cloud API"""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data.get_wav_data())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return ""

# ------------------ Commands ------------------
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Song {song} not found")
    elif "what is time" in c:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
    elif "shutdown" in c:
        speak("Shutting down your computer")
        os.system("shutdown /s /t 1")
    elif "restart" in c:
        speak("Restarting your computer")
        os.system("shutdown /r /t 1")
    elif "today news" in c:
        get_news()
    else:
        speak("Sorry, I didn't understand that command.")

# ------------------ News ------------------
def get_news():
    api_key = "ENTER YOUR API KEY"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    articles = requests.get(url).json().get("articles", [])
    if not articles:
        speak("Sorry, I couldn't fetch the news.")
    else:
        speak("Here are the top headlines.")
        for article in articles[:5]:
            speak(article['title'])

# ------------------ Main ------------------
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))