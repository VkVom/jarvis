import speech_recognition as sr
import pyttsx3
import pygame
import subprocess
import glob
import random
import psutil
import threading
import datetime
import vosk
import wave
import json

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

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
    model = vosk.Model("path_to_vosk_model")  # Path to Vosk model
    mic = sr.Microphone()
    
    with mic as source:
        print("Please speak something...")
        audio = recognizer.listen(source)
        
        # Save audio to a file
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
    # Transcribe with Vosk
    with wave.open("temp.wav", "rb") as wf:
        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                break
        result = rec.Result()
        text = json.loads(result).get("text", "")
    
    print("You said: " + text)
    return text

def open_application(app_name):
    try:
        if app_name.lower() == "notepad":
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
    text_to_speech("Hello, I am Jarvis, your AI assistant. How may I help you today?")
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
            elif "date" in command:
                get_date()
            elif "time" in command:
                get_time()
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
                text_to_speech("Thank you!")
                break
            else:
                text_to_speech("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    main_loop()
