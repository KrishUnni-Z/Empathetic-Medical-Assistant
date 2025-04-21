import os
import requests
from datetime import datetime
from transformers import pipeline
from streamlit_javascript import st_javascript

# Emotion classifier
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", top_k=1)

# User profile and context
profile_path = "user_profile.txt"
emotion_log_path = "emotion_log.txt"
user_profile = {"name": "", "age": "", "gender": "", "location": ""}
context_info = {"time": "", "location": "", "emotion": ""}

def load_profile():
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 3:
                user_profile["name"], user_profile["age"], user_profile["gender"] = lines[:3]
            if len(lines) >= 4:
                user_profile["location"] = lines[3]

def save_profile():
    with open(profile_path, "w") as f:
        f.write(f"{user_profile['name']}\n{user_profile['age']}\n{user_profile['gender']}\n{user_profile.get('location', '')}")

def get_time():
    js_code = """
    const now = new Date();
    const options = { weekday: 'long', hour: '2-digit', minute: '2-digit', hour12: true };
    const formatted = now.toLocaleString('en-US', options);
    window.parent.postMessage(formatted, '*');
    """
    return st_javascript(js_code, key="get_local_time") or "Local time unavailable"

def try_get_location():
    js_code = """
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        window.parent.postMessage({ lat: latitude, lon: longitude }, "*");
      },
      (err) => {
        window.parent.postMessage({ error: err.message }, "*");
      }
    );
    """
    coords = st_javascript(js_code, key="geo_location")
    if coords and isinstance(coords, dict) and "lat" in coords:
        return get_city_from_coords(coords["lat"], coords["lon"])
    return ""

def get_city_from_coords(lat, lon):
    try:
        res = requests.get(f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}")
        data = res.json()
        city = data.get("address", {}).get("city") or data.get("address", {}).get("town")
        state = data.get("address", {}).get("state", "")
        return f"{city}, {state}".strip(", ")
    except:
        return ""

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
