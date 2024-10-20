import cv2
import pytesseract
import pyttsx3
import speech_recognition as sr
from googlesearch import search
import webbrowser

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to David (male voice)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

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

def recognize_objects(frame):
    # Load pretrained model for object detection (can use Haarcascades for simplicity)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame

def read_text(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# Initialize the webcam
cap = cv2.VideoCapture(0)

text_to_speech("Hello, I am Jarvis. How can I assist you today?")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        frame = recognize_objects(frame)
        cv2.imshow('Camera', frame)
    elif key == ord('t'):
        text = read_text(frame)
        text_to_speech(f"I can read the following text: {text}")
        print(f"Text: {text}")
    elif key == ord('s'):
        user_query = speech_to_text()
        if user_query:
            results = list(search(user_query, num_results=1))
            if results:
                webbrowser.open(results[0])
                text_to_speech(f"Here is what I found: {results[0]}")

cap.release()
cv2.destroyAllWindows()
