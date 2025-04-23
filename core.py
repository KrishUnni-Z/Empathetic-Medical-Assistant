import os
import requests
from datetime import datetime
from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", top_k=1)

profile_path = "user_profile.txt"
emotion_log_path = "emotion_log.txt"

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
        return f"{res.get('city', '')}, {res.get('region', '')}"
    except:
        return "Unknown"

def get_emotion(text):
    try:
        result = emotion_classifier(text)
        label = result[0]["label"]
        score = result[0]["score"]
        log_emotion(label, score)
        return label
    except:
        return "neutral"

def log_emotion(label, score):
    try:
        with open(emotion_log_path, "a") as f:
            f.write(f"{datetime.now().isoformat()} - Emotion: {label}, Confidence: {score:.2f}\n")
    except:
        pass
