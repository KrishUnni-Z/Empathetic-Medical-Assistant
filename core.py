import os
import requests
from datetime import datetime
from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", top_k=1)

user_profile = {"name": "", "age": "", "gender": "", "location": ""}
context_info = {"time": "", "location": "", "emotion": ""}

profile_path = "user_profile.txt"
emotion_log_path = "emotion_log.txt"

def load_profile():
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            lines = f.read().splitlines()
            keys = list(user_profile.keys())
            for i in range(min(len(lines), len(keys))):
                user_profile[keys[i]] = lines[i]

def save_profile():
    with open(profile_path, "w") as f:
        for v in user_profile.values():
            f.write(v + "\n")

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("city", "") + ", " + res.get("region", "")
    except:
        return "Unknown"

def get_time(city="UTC"):
    try:
        res = requests.get(f"https://worldtimeapi.org/api/timezone")
        timezones = res.json()
        guess = next((tz for tz in timezones if city.lower() in tz.lower()), "Etc/UTC")
        time_data = requests.get(f"https://worldtimeapi.org/api/timezone/{guess}").json()
        dt = datetime.fromisoformat(time_data["datetime"].split("+")[0])
        return dt.strftime("%A, %I:%M %p")
    except:
        return datetime.now().strftime("%A, %I:%M %p")

def get_emotion(text):
    try:
        results = emotion_classifier(text)
        label = results[0]["label"]
        score = results[0]["score"]
        log_emotion(label, score)
        return label
    except:
        return "neutral"

def log_emotion(label, score):
    try:
        with open(emotion_log_path, "a") as log:
            log.write(f"{datetime.now().isoformat()} - Emotion: {label}, Confidence: {score:.2f}\n")
    except:
        pass
