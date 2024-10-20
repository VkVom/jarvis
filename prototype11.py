import cv2
import pyttsx3
import speech_recognition as sr

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize video capture from default camera (0)
cap = cv2.VideoCapture(0)

# Load object detection model (for demonstration, using Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variables for self-learning
unknown_object = None

# Speech recognizer
recognizer = sr.Recognizer()

# Loop to continuously capture frames
while True:
    # Read current frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale for object detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame using Haar Cascade (for demonstration)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow('Object Recognition', frame)
    
    # Use speech recognition to listen for user input
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
        try:
            query = recognizer.recognize_google(audio).lower()
            print(f"User Query: {query}")
            
            # Process user query
            if "what is it" in query:
                if unknown_object:
                    speak(f"It's a {unknown_object}.")
                else:
                    speak("I don't know what it is. Can you tell me?")
                    audio = recognizer.listen(source)
                    object_name = recognizer.recognize_google(audio).lower()
                    print(f"User Response: {object_name}")
                    speak(f"Thanks for teaching me. Now I know it's a {object_name}.")
                    unknown_object = object_name
            
            # Exit loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
