# Empathetic Medical Assistant

**Empathetic Medical Assistant** is a conversational AI application developed to support users experiencing emotional or health-related distress. It delivers emotionally aware responses that adapt based on user input, emotional tone, and contextual factors like time, location, and weather. This tool is not intended to provide diagnoses, but to offer comfort, support, and guidance toward seeking professional help when needed.

**Live Application**: [https://empathetic-medical-assistant.streamlit.app](https://empathetic-medical-assistant.streamlit.app)  
**Team**: 14  
**University**: University of Technology Sydney  
**Subject**: 36118 – Applied Natural Language Processing (Autumn 2025)

## Project Objective

The primary aim of this project is to explore how natural language processing can be applied to simulate empathetic, emotionally intelligent dialogue in a non-clinical setting. The assistant is designed to act as a supportive companion for users dealing with psychological or physical discomfort. It does so by integrating emotion classification, context-awareness (such as weather, time, and location), and role-based conversational agents. 

The assistant does not provide medical diagnosis. Instead, it demonstrates how a multi-agent chatbot architecture can promote psychological safety, offer motivational guidance, and route users to further help if needed. The broader goal is to showcase a lightweight, modular, and ethical approach to empathetic conversational design using real-time NLP techniques.

## Key Features

### Emotion-Aware Dialogue

The assistant detects emotions in the user's message using the `bert-base-go-emotion` model. Based on detected emotions such as sadness, fear, or anger, it selects appropriate language, tone, and behavior. For high-risk emotions, a safety-first agent is triggered.

### Contextual Awareness

Responses are influenced by environmental and personal context, including:

- Name, age, and gender of the user
- Current local time and location (based on IP)
- Real-time weather conditions (temperature and description)

This context is reflected in the conversation, allowing for more relevant and personalized support.

### Agent-Based Architecture

The assistant dynamically switches between five specialized agents:

1. **Welcome Agent**: Greets users and encourages them to share
2. **Threat Agent**: Engages in calm, reassuring dialogue when distress is detected
3. **Chat Agent**: Handles ongoing conversation based on prior messages
4. **Appointment Agent**: Gently recommends seeking help and suggests next steps
5. **Conclusion Agent**: Provides closure with affirming language and motivational quotes

### Profile and Session Management

- A one-time profile form allows the user to enter their name, age, and gender
- Profile information is displayed in the sidebar throughout the session
- Options are provided to reset the profile or clear the chat at any time

### Interface and User Experience

- The assistant is deployed as a web application using Streamlit
- Chat history is retained during the session to preserve continuity
- The user interface is responsive and includes a light or dark mode toggle
- Font size and layout are optimized for readability and comfort

## Technical Components

- Built with Streamlit for the user interface
- Uses Hugging Face Transformers for emotion classification
- Utilizes the OpenAI Agents SDK for conversational agent management
- Connects to OpenAI’s GPT model via GitHub Token and Azure Inference API
- Emotion logs and profile data are managed with lightweight local storage

## Intended Use Case

This assistant is designed for users seeking a compassionate listener or first layer of support. It is suitable for use cases such as wellness check-ins, non-clinical conversations about stress or mood, and general emotional support. It is not a replacement for professional medical advice or intervention.

## Credits

This project was developed by Team 14 for the subject Applied Natural Language Processing (36118) at the University of Technology Sydney, Autumn 2025.
