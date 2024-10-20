import speech_recognition as sr
import pyttsx3
import pygame
import os
import subprocess
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import requests
import glob
import random

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

# Configure the Selenium WebDriver
chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service)

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
            print(f"Sorry, I don't know how to open {app_name}.")
            text_to_speech(f"Sorry, I don't know how to open {app_name}.")
    except Exception as e:
        print(f"An error occurred while trying to open {app_name}: {e}")
        text_to_speech(f"An error occurred while trying to open {app_name}.")

def close_application(app_name):
    try:
        if app_name.lower() == "chrome":
            driver.quit()
        elif app_name.lower() == "notepad":
            os.system("taskkill /f /im notepad.exe")
        elif app_name.lower() == "music":
            pygame.mixer.music.stop()
        else:
            print(f"Sorry, I don't know how to close {app_name}.")
            text_to_speech(f"Sorry, I don't know how to close {app_name}.")
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

def play_local_song(song_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
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

if __name__ == "__main__":
    text_to_speech("Hello, I am Jarvis. How can I assist you today?")
    while True:
        print("Say 'exit' to quit.")
        user_input = speech_to_text()
        if user_input:
            if "exit" in user_input.lower():
                break
            elif user_input.lower().startswith("open"):
                app_name = user_input[5:].strip()  # Get the app name after "open "
                open_application(app_name)
            elif user_input.lower().startswith("close"):
                app_name = user_input[6:].strip()  # Get the app name after "close "
                close_application(app_name)
            elif user_input.lower().startswith("search"):
                query = user_input[7:].strip()  # Get the query after "search "
                result = search_online(query)
                if result:
                    text_to_speech(f"Here is what I found: {result}")
            elif user_input.lower().startswith("play song"):
                play_random_local_song()
