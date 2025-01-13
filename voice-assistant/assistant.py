import os
import tkinter as tk
from tkinter import ttk
import openai 
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listens for user input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            result_label.config(text="Listening...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        
# Generates a response based on user input
def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"
    
def process_command():
    user_command = listen()
    result_label.config(text=f"You said: {user_command}")
    if user_command:
        # Generates the AI response
        response = generate_response(f"User said: {user_command}. Respond like a helpful assistant.")
        result_label.config(text=f"Response: {response}")
        speak(response)
        animate_text(response)

# Function to animate the text 
def animate_text(text):
    result_label.config(text="")
    def update_text(index=0):
        if index < len(text):
            result_label.config(text=result_label.cget("text") + text[index])
            root.after(50, update_text, index + 1)
    update_text()

# Setting up the GUI
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x400")

style = ttk.Style()
style.configure("TButton", font=("Arial", 16))

title_label = tk.Label(root, text="Voice Assistant", font=("Arial", 24))
title_label.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 16), wraplength=500)
result_label.pack(pady=20)

listen_button = ttk.Button(root, text="Listen", command=process_command)
listen_button.pack(pady=20)

exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()