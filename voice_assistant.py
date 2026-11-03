
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import soundfile as sf
import webbrowser
import datetime
import subprocess
import urllib.parse

engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    try:
        speak("Listening. Please speak.")

        audio_data = sd.rec(
            int(5 * 16000),
            samplerate=16000,
            channels=1,
            dtype="int16",
            device=1
        )
        sd.wait()
        sf.write("recording.wav", audio_data, 16000)

        with sr.AudioFile("recording.wav") as source:
            audio = recognizer.record(source)

        command = recognizer.recognize_google(
            audio, language="en-IN"
        )
        print("You said:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        speak("Internet connection problem.")
        return ""
    except Exception as e:
        print("Error:", e)
        speak("Something went wrong.")
        return ""

def run_assistant():
    speak("Hello! I am your personal voice assistant.")

    while True:
        command = listen()

        if not command:
            continue

        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The time is " + current_time)

        elif "date" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + today)

        elif "good morning" in command:
            speak("Good morning! Have a great day.")

        elif "good evening" in command:
            speak("Good evening! How can I help you?")

        elif "youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "search" in command:
            query = command.replace("search", "", 1).strip()
            if query:
                speak("Searching Google for " + query)
                url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
                webbrowser.open(url)
            else:
                speak("Please tell me what to search.")

        elif "google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "notepad" in command:
            speak("Opening Notepad.")
            subprocess.Popen("notepad.exe")

        elif "hello" in command:
            speak("Hello! How can I help you?")

        else:
            speak("Sorry, command not recognized.")

if __name__ == "__main__":
    run_assistant()