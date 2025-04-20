import os
import streamlit as st
import requests
from datetime import datetime
from transformers import pipeline

# Emotion classifier
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", top_k=1)

# Paths
profile_path = "user_profile.txt"
emotion_log_path = "emotion_log.txt"

# Global state
user_profile = {"name": "", "age": "", "gender": ""}
context_info = {"time": "", "location": "", "emotion": ""}

def load_profile():
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 3:
                user_profile["name"], user_profile["age"], user_profile["gender"] = lines[:3]

def save_profile():
    with open(profile_path, "w") as f:
        f.write(f"{user_profile['name']}\n{user_profile['age']}\n{user_profile['gender']}")

def get_time():
    return datetime.now().strftime("%A, %I:%M %p")

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("city", "") + ", " + res.get("region", "")
    except:
        return "Unknown location"

def get_weather():
    try:
        key = st.secrets["OPENWEATHER_API_KEY"]
        loc = get_location().split(",")[0]
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={key}&units=metric"
        weather_data = requests.get(weather_url).json()
        desc = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        return f"{desc}, {temp}°C"
    except:
        return "weather unavailable"

def get_emotion(text):
    try:
        results = emotion_classifier(text)
        label = results[0]["label"]
        score = results[0]["score"]
        log_emotion(label, score)
        if label in ["despair", "suicidal", "fear", "anger", "sadness"] and score > 0.7:
            return label
        return label
    except:
        return "neutral"

def log_emotion(label, score):
    try:
        with open(emotion_log_path, "a") as log:
            log.write(f"{datetime.now().isoformat()} - Emotion: {label}, Confidence: {score:.2f}\n")
    except:
        pass
