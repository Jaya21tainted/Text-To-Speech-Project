import os
import speech_recognition as sr
from gtts import gTTS
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function for Text-to-Speech (TTS)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("static/output.mp3")  # Save as MP3 file

# Function for Speech-to-Text (STT)
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert-text', methods=['POST'])
def convert_text():
    text = request.form['text']
    text_to_speech(text)
    return jsonify({"message": "Text converted to speech!", "audio": "static/output.mp3"})

@app.route('/convert-speech', methods=['POST'])
def convert_speech():
    recognized_text = speech_to_text()
    return jsonify({"message": "Speech converted to text!", "text": recognized_text})

if __name__ == "__main__":
    app.run(debug=True)
