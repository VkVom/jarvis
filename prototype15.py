import speech_recognition as sr
import pyttsx3
import pygame
import subprocess
import webbrowser
from googlesearch import search
import time
import datetime
import requests
import glob
import random
from bs4 import BeautifulSoup
import psutil
import threading

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

HERE_API_KEY = "_NpREfG7O1gEViO-Wwmv3Rx5Hzuix8UY2CodCdt2ZXs"
HERE_API_ID = "CT4Do4rzbxyF6DjmxXbC"
master_name = "G O A T      the greatest of all time"

# Initialize pygame mixer
pygame.mixer.init()
music_thread = None
stop_event = threading.Event()

def text_to_speech(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None

def open_application(app_name):
    try:
        if app_name.lower() == "google":
            subprocess.Popen(["start", "chrome"], shell=True)
        elif app_name.lower() == "youtube":
            subprocess.Popen(["start", "chrome", "https://www.youtube.com"], shell=True)
        elif app_name.lower() == "notepad":
            subprocess.Popen(["notepad"])
        elif app_name.lower() == "calculator":
            subprocess.Popen(["calc"])
        else:
            subprocess.Popen(["start", app_name], shell=True)
    except Exception as e:
        print(f"An error occurred while trying to open {app_name}: {e}")
        text_to_speech(f"An error occurred while trying to open {app_name}.")

def close_application(app_name):
    try:
        app_name = app_name.lower()
        found = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower() if 'name' in proc.info else ''
                proc_cmdline = proc.info['cmdline'] if 'cmdline' in proc.info else []
                
                if app_name in proc_name or any(app_name in cmd_part.lower() for cmd_part in proc_cmdline):
                    proc.kill()
                    text_to_speech(f"{proc_name} has been closed.")
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if not found:
            text_to_speech(f"Sorry, I couldn't find any application named {app_name} to close.")
    except Exception as e:
        print(f"An error occurred while trying to close {app_name}: {e}")
        text_to_speech(f"An error occurred while trying to close {app_name}.")

def search_online(query):
    try:
        search_results = list(search(query, num_results=1))
        if search_results:
            webbrowser.open(search_results[0])
            return search_results[0]
        else:
            text_to_speech("I'm sorry, I couldn't find the information you're looking for.")
            return None
    except Exception as e:
        print(f"An error occurred while searching online: {e}")
        text_to_speech(f"An error occurred while searching online: {e}")
        return None

def search_and_say(query):
    try:
        search_results = list(search(query, num_results=1))
        if search_results:
            response = requests.get(search_results[0])
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([para.text for para in paragraphs[:3]])
            if content:
                text_to_speech(content)
                return content
            else:
                text_to_speech("I couldn't find any readable content on the page.")
                return None
        else:
            text_to_speech("I'm sorry, I couldn't find the information you're looking for.")
            return None
    except Exception as e:
        print(f"An error occurred while searching and fetching the content: {e}")
        text_to_speech(f"An error occurred while searching and fetching the content: {e}")
        return None

def play_local_song(song_path):
    global music_thread, stop_event
    stop_event.clear()
    def play_song():
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and not stop_event.is_set():
                continue
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"An error occurred while playing the song: {e}")
            text_to_speech(f"An error occurred while playing the song.")
    music_thread = threading.Thread(target=play_song)
    music_thread.start()

def play_random_local_song():
    try:
        songs_folder = r'C:\Users\Dell\Music\songs'
        songs = glob.glob(songs_folder + '/*.mp3')
        if songs:
            song_to_play = random.choice(songs)
            play_local_song(song_to_play)
        else:
            print("No songs found in the specified directory.")
            text_to_speech("No songs found in the specified directory.")
    except Exception as e:
        print(f"An error occurred while playing a random song: {e}")
        text_to_speech(f"An error occurred while playing a random song.")

def play_specific_local_song(song_name):
    try:
        songs_folder = r'C:\Users\Dell\Music\songs'
        songs = glob.glob(songs_folder + f'/*{song_name}*.mp3')
        if songs:
            song_to_play = songs[0]  # Play the first matching song
            play_local_song(song_to_play)
        else:
            print(f"No song named {song_name} found in the specified directory.")
            text_to_speech(f"No song named {song_name} found in the specified directory.")
    except Exception as e:
        print(f"An error occurred while playing the song {song_name}: {e}")
        text_to_speech(f"An error occurred while playing the song {song_name}.")

def stop_song():
    global stop_event
    if pygame.mixer.music.get_busy():
        stop_event.set()
        pygame.mixer.music.stop()

def get_date():
    today = datetime.date.today()
    text_to_speech(f"Today's date is {today.strftime('%B %d, %Y')}")
    return today

def get_time():
    now = datetime.datetime.now().time()
    text_to_speech(f"The current time is {now.strftime('%H:%M:%S')}")
    return now

def get_weather(location):
    base_url = f"https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey={HERE_API_KEY}&product=observation&name={location}"
    try:
        response = requests.get(base_url)
        data = response.json()
        if "observations" in data and "location" in data["observations"]:
            location_data = data["observations"]["location"][0]
            weather_desc = location_data["observation"][0]["description"]
            temp = location_data["observation"][0]["temperature"]
            text_to_speech(f"The weather in {location} is {weather_desc} with a temperature of {temp} Celsius.")
            return weather_desc, temp
        else:
            text_to_speech("City not found.")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the weather: {e}")
        text_to_speech(f"An error occurred while fetching the weather: {e}")
        return None

def get_news():
    api_key = "d4213188f63b49c8b98f9336fefeaa0d"  # Replace with your NewsAPI key
    base_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(base_url)
        articles = response.json()["articles"]
        headlines = [article["title"] for article in articles[:5]]
        for headline in headlines:
            text_to_speech(headline)
        return headlines
    except Exception as e:
        print(f"An error occurred while fetching the news: {e}")
        text_to_speech(f"An error occurred while fetching the news: {e}")
        return None

def get_location():
    try:
        response = requests.get(f"https://ipapi.co/json/")
        data = response.json()
        location = f"{data['city']}, {data['region']}, {data['country_name']}"
        text_to_speech(f"Your current location is {location}")
        return location
    except Exception as e:
        print(f"An error occurred while fetching the location: {e}")
        text_to_speech(f"An error occurred while fetching the location: {e}")
        return None

def change_boss(new_boss_name):
    global master_name
    master_name = new_boss_name
    text_to_speech(f"I have a new boss now. Hello, {new_boss_name}!")

def respond_to_greeting():
    greetings = ["Hello!", "Hi there!", "Greetings!", "How can I assist you today?"]
    text_to_speech(random.choice(greetings))

def respond_to_thanks():
    responses = ["You're welcome!", "No problem!", "Happy to help!", "Anytime!"]
    text_to_speech(random.choice(responses))

def main_loop():
    global music_thread
    while True:
        print("Listening for command...")
        command = speech_to_text()
        if command:
            command = command.lower()

            if "open" in command:
                app_name = command.replace("open", "").strip()
                open_application(app_name)
            elif "close" in command:
                app_name = command.replace("close", "").strip()
                close_application(app_name)
            elif "search" in command:
                query = command.replace("search", "").strip()
                search_online(query)
            elif "date" in command:
                get_date()
            elif "time" in command:
                get_time()
            elif "weather" in command:
                if "in" in command:
                    location = command.split("in")[-1].strip()
                    get_weather(location)
                else:
                    get_weather("current location")
            elif "news" in command:
                get_news()
            elif "location" in command:
                get_location()
            elif "who is your boss" in command:
                text_to_speech(f"My boss is {master_name}.")
            elif "change boss" in command:
                text_to_speech("Who is my new boss?")
                new_boss_name = speech_to_text()
                if new_boss_name:
                    change_boss(new_boss_name)
            elif "play song" in command:
                play_random_local_song()
            elif "jarvis play" in command:
                song_name = command.replace("jarvis play", "").strip()
                play_specific_local_song(song_name)
            elif "change song" in command:
                if music_thread and music_thread.is_alive():
                    stop_song()
                play_random_local_song()
            elif "stop song" in command or "exit song" in command:
                stop_song()
            elif "hello" in command or "hi" in command:
                respond_to_greeting()
            elif "thank you" in command or "thanks" in command:
                respond_to_thanks()
            elif "exit" in command:
                text_to_speech("Goodbye!")
                break
            else:
                text_to_speech("I'm sorry, I didn't understand that command.")
                
if __name__ == "__main__":
    main_loop()
