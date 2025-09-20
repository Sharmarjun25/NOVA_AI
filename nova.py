import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from ollama import Client
import os
import subprocess
import time
from gtts import gTTS
import pygame
from dotenv import load_dotenv
from datetime import datetime
#import pyttsx3
import random
import psutil

#engine = pyttsx3.init()

recognizer = sr.Recognizer()
load_dotenv()
ollama_client = Client(host='http://localhost:11434')
newsapi = os.getenv("NEWS_API_KEY")
weatherapi = os.getenv("WEATHER_API_KEY")

'''def speak(text):
    print(f"Nova:{text}")
    engine.say(text)
    engine.runAndWait()'''

def speak(text):
    print(f"NOVA : {text}")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        
        #pygame.mixer.init()
        #pygame.mixer.music.load("temp.mp3")
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
          #  time.sleep(0.1)  # wait while playing
        os.system("start temp.mp3") 
    except Exception as e:
        print(f"TTS Error: {e}")


def aiProcess(command):
    response = ollama_client.chat(
        model='phi3',
        messages=[
            {"role": "system", "content": "You are Nova, a helpful offline virtual assistant skilled in general tasks like Alexa and Google Assistant."},
            {"role": "user", "content": command}
        ]
    )
    return response['message']['content']


def get_weather(city_name):
    if not weatherapi:
        return "Weather API key not found."
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weatherapi}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()

        if data["cod"]!=200:
            return "City not found. Try again."
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        result = f"The current temperature in {city_name} is {temp}°C with {weather_description}. Humidity is {humidity}%."
        return result
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
    

def system_monitor():
    cpu = psutil.cpu_percent(interval = 1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    info = f"CPU Usage is {cpu}% , RAM Usage is {ram}% , Disk Usage is{disk}%"
    print(info)
    speak(info)

def search_file(filename , search_path = "C:\\"):
        found_files = []
        for root , dirs , files in os.walk(search_path):
            if filename.lower() in map(str.lower , files):
                found_files.append(os.path.join(root , filename))
        if found_files:
            speak(f"Found {len(found_files)} file(s). Showing top 5 results:")
            for f in found_files[:5]:
                print(f)
        else:
            speak("No file found with this name.")

def processCommand(c):
    if "open google" in c.lower():
        speak("Google opened")
        time.sleep(0.2)
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("facebook opened")
        time.sleep(0.2)
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Youtube opened")
        time.sleep(0.2)
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        speak(" Instagram opened")
        time.sleep(0.2)
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        speak("linkedin opened")
        time.sleep(0.2)
        webbrowser.open("https://linkedin.com")
    elif "open gpt" in c.lower():
        speak("chatgpt opened")
        time.sleep(0.2)
        webbrowser.open("https://chatgpt.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
            time.sleep(0.2)
        else:
            speak("Sorry , I could not find that song in your library.")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json() #parse the json articles
            articles = data.get('articles' , [])
            # above wqas used to extract the articles
            #to print
            for article in articles[:4]: #to just limit the use of articles thats why [:5] is used
                print(article['title'])
                speak(article['title'])

    elif "weather" in c.lower():
        words = c.split()
        city_name = None
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city_name  = " ".join(words[city_index:])
        if city_name:
            weather_info = get_weather(city_name)
            speak(weather_info)
        else:
            speak("Please tell me city name !")

    # TO DO SOME BASIC OPERATIONS IN MY SYSTEM
    elif "open this pc" in c.lower():
        speak("Opening this PC")
        time.sleep(0.2)
        subprocess.Popen("explorer")
    elif "open settings" in c.lower():
        speak("Opening settings")
        time.sleep(0.2)
        subprocess.Popen("start ms-settings:",shell=True)
    elif "open notepad" in c.lower():
        speak("Opening Notepad.")
        time.sleep(0.2)
        subprocess.Popen("notepad")
    elif "open calculator" in c.lower():
        speak("Opening Calculator.")
        time.sleep(0.2)
        subprocess.Popen("calc")
    elif "time" in c.lower() or "date" in c.lower():
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%B %d, %Y")
        speak(f"Sir , the current time is {current_time} and today's date is {current_date}")

    elif "system monitor" in c.lower() or "system status" in c.lower():
        system_monitor()

    elif "search file" in c.lower():
        speak("tell me the file name to search")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source , timeout=10)
                filename = recognizer.recognize_google(audio).lower()
                search_file(filename)
        except Exception as e:
            speak(f"Error in file search : {e}")
    
    else:
         output = aiProcess(c)
         speak(output)

if __name__ == "__main__":
    speak("Welcome Sir ! How may i help you   ")
    while True:
    #listen for the wake word Nova
    #obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word nova..")
                audio = r.listen(source , timeout=2 , phrase_time_limit=1)
                command = r.recognize_google(audio).lower()
                if(command.lower() == "nova"):
                    speak("Yes")
                    #Listen for command 
                    with sr.Microphone() as source:
                        print("Nova active...Waiting for your command.. ")
                        audio = r.listen(source , timeout=15) 
                        command = r.recognize_google(audio).lower()
                        print("You said:" , command)

                        processCommand(command)


        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error;{e}")
