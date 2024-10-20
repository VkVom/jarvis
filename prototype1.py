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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import requests

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

# Configure the Selenium WebDriver (ensure you have the correct driver for your browser)
chrome_driver = ChromeDriverManager().install()
chrome_service = ChromeService(executable_path=chrome_driver)
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
        if app_name.lower() == "google":
            os.system("taskkill /f /im chrome.exe")
        elif app_name.lower() == "notepad":
            os.system("taskkill /f /im notepad.exe")
        elif app_name.lower() == "calculator":
            os.system("taskkill /f /im calculator.exe")
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

def open_gmail():
    try:
        driver.get("https://mail.google.com/")
        text_to_speech("Gmail is open. Please log in if not already logged in.")
        time.sleep(15)  # Wait for the user to log in
    except Exception as e:
        print(f"An error occurred while opening Gmail: {e}")
        text_to_speech(f"An error occurred while opening Gmail: {e}")

def type_email_content():
    try:
        text_to_speech("What is the recipient's email address?")
        recipient = speech_to_text()
        if not recipient:
            return
        
        text_to_speech("What is the subject?")
        subject = speech_to_text()
        if not subject:
            return
        
        text_to_speech("What is the body of the email?")
        body = speech_to_text()
        if not body:
            return

        compose_button = driver.find_element_by_xpath("//div[@role='button'][text()='Compose']")
        compose_button.click()
        time.sleep(5)  # Wait for the compose window to open
        
        to_field = driver.find_element_by_name("to")
        to_field.send_keys(recipient)
        
        subject_field = driver.find_element_by_name("subjectbox")
        subject_field.send_keys(subject)
        
        body_field = driver.find_element_by_xpath("//div[@aria-label='Message Body']")
        body_field.send_keys(body)
        
        text_to_speech("Email content has been typed.")
    except Exception as e:
        print(f"An error occurred while typing email content: {e}")
        text_to_speech(f"An error occurred while typing email content: {e}")

def send_email():
    try:
        send_button = driver.find_element_by_xpath("//div[@role='button'][text()='Send']")
        send_button.click()
        text_to_speech("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        text_to_speech(f"An error occurred while sending the email: {e}")

def get_date():
    today = datetime.date.today()
    text_to_speech(f"Today's date is {today.strftime('%B %d, %Y')}")
    return today

def get_time():
    now = datetime.datetime.now().time()
    text_to_speech(f"The current time is {now.strftime('%H:%M:%S')}")
    return now

def get_weather(location="New York"):
    api_key = "c62e1dbb0715dd6fe8924a33e84b49f7"  # Replace with your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            text_to_speech(f"The weather in {location} is {weather_desc} with a temperature of {temp} Kelvin.")
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

if __name__ == "__main__":
    text_to_speech("Hello, I am Jarvis. How can I assist you today?")
    while True:
        print("Say 'exit' to quit.")
        user_input = speech_to_text()
        if user_input:
            if "exit" in user_input.lower():
                break
            elif user_input.lower().startswith("open"):
                app_name = user_input[5:]  # Get the app name after "open "
                open_application(app_name.strip())
            elif user_input.lower().startswith("close"):
                app_name = user_input[6:]  # Get the app name after "close "
                close_application(app_name.strip())
            elif user_input.lower().startswith("search"):
                query = user_input[7:]  # Get the query after "search "
                result = search_online(query.strip())
                if result:
                    text_to_speech(f"Here is what I found: {result}")
            elif "compose email" in user_input.lower():
                open_gmail()
            elif "send email" in user_input.lower():
                send_email()
            elif "tell me the date" in user_input.lower():
                get_date()
            elif "tell me the time" in user_input.lower():
                get_time()
            elif "tell me the weather" in user_input.lower():
                get_weather()
            elif "tell me the news" in user_input.lower():
                get_news()
