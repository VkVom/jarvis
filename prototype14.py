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
import json
import threading

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

# Initialize Pygame Mixer for Music Playback
pygame.mixer.init()

HERE_API_KEY = "_NpREfG7O1gEViO-Wwmv3Rx5Hzuix8UY2CodCdt2ZXs"
HERE_API_ID = "CT4Do4rzbxyF6DjmxXbC"
master_name = "G O A T      the greatest of all time"

# Initialize music_thread to None
music_thread = None

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
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"An error occurred while playing the song: {e}")
        text_to_speech(f"An error occurred while playing the song.")

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

def change_song():
    try:
        play_random_local_song()
    except Exception as e:
        print(f"An error occurred while changing the song: {e}")
        text_to_speech(f"An error occurred while changing the song.")

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

def get_weather_of_current_location():
    try:
        response = requests.get(f"https://ipapi.co/json/")
        data = response.json()
        latitude = data['latitude']
        longitude = data['longitude']

        weather_url = f"https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey={HERE_API_KEY}&product=observation&latitude={latitude}&longitude={longitude}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if "observations" in weather_data and "location" in weather_data["observations"]:
            location = weather_data["observations"]["location"][0]
            weather_desc = location["observation"][0]["description"]
            temp = location["observation"][0]["temperature"]
            text_to_speech(f"The weather at your location is {weather_desc} with a temperature of {temp} Celsius.")
            return weather_desc, temp
        else:
            text_to_speech("I could not fetch the weather details for your location.")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the weather of current location: {e}")
        text_to_speech(f"An error occurred while fetching the weather of current location: {e}")
        return None

def respond_to_greeting(greeting):
    responses = [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Greetings! How may I assist you?",
    ]
    text_to_speech(random.choice(responses))

def express_gratitude():
    responses = [
        "You're welcome!",
        "No problem!",
        "Anytime!",
        "Happy to help!",
    ]
    text_to_speech(random.choice(responses))

def have_friendly_conversation(statement):
    responses = [
        "That's interesting! Tell me more.",
        "I see! What else is on your mind?",
        "I'm glad you shared that with me.",
    ]
    text_to_speech(random.choice(responses))

def stop_execution():
    text_to_speech("Stopping the current task. What would you like to do next?")

def handle_boss_query(query):
    global master_name
    if query.lower() == "who is your boss":
        text_to_speech(f"My boss is {master_name}.")
    elif query.lower() == "change boss":
        text_to_speech("Who is my new boss?")
        new_boss = speech_to_text()
        if new_boss:
            master_name = new_boss
            text_to_speech(f"My boss is now {master_name}.")

def main_loop():
    global music_thread
    if music_thread and music_thread.is_alive():
        pygame.mixer.music.stop()
        music_thread.join()

    text_to_speech("Hello, I am Jarvis. How can I assist you today?")
    
    while True:
        print("Say 'exit' to quit.")
        user_input = speech_to_text()
        
        if user_input is None:
            continue

        user_input = user_input.lower()

        if 'play' in user_input and 'song' in user_input:
            if music_thread and music_thread.is_alive():
                pygame.mixer.music.stop()
                music_thread.join()
            music_thread = threading.Thread(target=play_random_local_song)
            music_thread.start()
        
        elif 'change song' in user_input:
            if music_thread and music_thread.is_alive():
                pygame.mixer.music.stop()
                music_thread.join()
            music_thread = threading.Thread(target=change_song)
            music_thread.start()
        
        elif 'stop' in user_input and 'song' in user_input:
            if music_thread and music_thread.is_alive():
                pygame.mixer.music.stop()
                music_thread.join()
        
        elif user_input == 'exit':
            if music_thread and music_thread.is_alive():
                pygame.mixer.music.stop()
                music_thread.join()
            break
        
        elif 'open' in user_input:
            app_name = user_input.split('open ')[-1]
            open_application(app_name)
        
        elif 'close' in user_input:
            app_name = user_input.split('close ')[-1]
            close_application(app_name)
        
        elif 'search' in user_input:
            query = user_input.split('search ')[-1]
            search_online(query)
        
        elif 'news' in user_input:
            get_news()
        
        elif 'date' in user_input:
            get_date()
        
        elif 'time' in user_input:
            get_time()
        
        elif 'weather' in user_input and 'location' in user_input:
            location = user_input.split('weather in ')[-1]
            get_weather(location)
        
        elif 'weather' in user_input:
            get_weather_of_current_location()
        
        elif 'location' in user_input:
            get_location()
        
        elif 'greeting' in user_input:
            respond_to_greeting(user_input)
        
        elif 'thank you' in user_input or 'thanks' in user_input:
            express_gratitude()
        
        elif 'who is your boss' in user_input or 'change boss' in user_input:
            handle_boss_query(user_input)
        
        else:
            have_friendly_conversation(user_input)

if __name__ == "__main__":
    main_loop()
