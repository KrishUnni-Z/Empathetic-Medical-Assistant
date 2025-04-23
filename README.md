
# Empathetic Medical Assistant

Empathetic Medical Assistant is a modular conversational AI application designed to provide emotional support through empathetic, non-diagnostic conversations. The chatbot uses pre-trained large language models (LLMs) and real-time emotion classification to detect tone, personalize responses, and route conversations safely.

This system is not intended to diagnose or treat medical conditions. It provides a friendly and emotionally intelligent companion that can guide users toward reflection, support, or professional help when appropriate.

## Live Demo
Streamlit App: https://empathetic-medical-assistant.streamlit.app

## Project Objective

The primary goal of this project was to design and implement an empathetic medical assistant chatbot capable of responding to users in a psychologically safe, emotionally supportive manner. The aim was not to provide clinical diagnosis, but to simulate conversations that acknowledge emotional distress, offer comfort, and encourage users to seek real-world help when needed.

To achieve this, we explored the use of pre-trained large language models (LLMs) in a modular, multi-agent architecture. This approach allowed us to generate natural, personalized responses while maintaining ethical boundaries and avoiding risky advice. The chatbot dynamically adjusted its tone and behavior based on detected emotional states, user profile data, and contextual cues such as time and location.

Our implementation focused on creating a conversation system that is:
- Emotionally intelligent and non-judgmental  
- Safe for use in non-clinical wellness check-ins  
- Flexible enough to handle both casual and critical user inputs  
- Fully modular with clearly defined agent responsibilities  
- Real-time deployable with no need for custom training or fine-tuning

This project demonstrates how LLMs can be effectively applied to support empathetic dialogue when paired with proper moderation, ethical controls, and a supportive conversation framework.

## Team and Context

- Team Number: 14  
- Course: 36118 – Applied Natural Language Processing  
- University: University of Technology Sydney  
- Session: Autumn 2025

## Key Features

### Emotion Detection and Routing  
- Uses a pre-trained emotion classifier (GoEmotions via Hugging Face) to detect user emotion in real time  
- Emotion influences agent selection:  
  - Sadness, fear, despair → ThreatAgent  
  - Joy, neutral, casual → ChatAgent  

### Multi-Agent Conversational Design  
- WelcomeAgent: Greets the user and sets the tone  
- ChatAgent: Handles ongoing dialogue in neutral/positive states  
- ThreatAgent: Responds to emotionally intense or high-risk messages  
- AppointmentAgent: Offers help suggestions or mental health resources  
- ConclusionAgent: Ends the session with motivational quotes  

### Context Awareness  
- User details (name, age, gender)  
- Current time and geographic location  
- Personalized tone and suggestions using context without fine-tuning  

### Moderation Fallback  
- If a user's message triggers Azure moderation, the assistant captures the block reason and safely redirects to the ThreatAgent  
- No flagged content is reprocessed — fallback uses a neutral input for safety

## How to Run Locally

You’ll need your own GitHub Azure Inference API token to run this locally.

### 1. Clone the repository

git clone https://github.com/your-username/empathetic-medical-assistant.git  
cd empathetic-medical-assistant

### 2. Set up your API token in Streamlit

Create a file at `.streamlit/secrets.toml` and add:

GITHUB_TOKEN = "your_inference_api_token"

Get your token from Azure or GitHub's OpenAI plugin registration page.

### 3. Install dependencies

python -m venv venv  
source venv/bin/activate  # or venv\Scripts\activate on Windows  
pip install -r requirements.txt

### 4. Run the app

streamlit run app.py

## Architecture Overview

- Built with Streamlit  
- Uses OpenAI Agents SDK for modular agent roles  
- Emotion classification via Hugging Face Transformers  
- GPT model served through Azure OpenAI (GitHub token inference endpoint)  
- Lightweight local storage for user profile and emotion logs  
- Visual safety fallback in case of moderation blocks

## What This Project Does Not Do

- Does not train or fine-tune LLMs  
- Does not diagnose or provide clinical decisions  
- Does not retrieve real-time medical or weather data (except location via IP)  
- Does not use any datasets directly from Kaggle or external APIs during chat

## What This Project Demonstrates

- Modular, real-time emotion-aware conversations  
- Secure fallback handling for sensitive content  
- Responsible AI practices under Azure moderation policy  
- Streamlit-based rapid prototyping for NLP-powered tools

## File Structure

- app.py – Main Streamlit frontend interface  
- core.py – Emotion logging, profile handling, location/time  
- chat_agents.py – Role-based agent logic  
- config.py – Model and token setup for OpenAI SDK  
- user_profile.txt – Local profile persistence  
- emotion_log.txt – Optional logging for debug/safety review  

## Acknowledgements

Developed collaboratively by Team 14 for the Applied NLP course project at UTS. This project was focused on safety-first conversational design and applied LLM evaluation.

The project uses:
- OpenAI GPT-4o
- Hugging Face Emotion Classifier
- Streamlit
- Azure OpenAI Inference
