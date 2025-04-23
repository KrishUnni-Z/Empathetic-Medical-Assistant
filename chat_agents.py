from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    return Agent(name="WelcomeAgent", instructions=f"""
    Greet {user_profile['name']} warmly. They are a {user_profile['age']} year old {user_profile['gender']}.
    They are currently in {context_info['location']} and it is {context_info['time']}.
    Your tone should be friendly, soft, and supportive.
    Suggest gentle lifestyle tips, and remind them this is a safe space to talk.
    You are not a doctor, so do not diagnose. Encourage medical follow-up for real symptoms.
    """)

def threat_agent(user_input=""):
    emotion = context_info.get("emotion", "fear")
    return Agent(name="ThreatAgent", instructions=f"""
    The user expressed potential danger or emotional crisis. Detected emotion: {emotion}.
    Do NOT provide medical advice. Instead:
    - Show concern
    - Validate feelings
    - Recommend speaking to a trusted person or helpline
    - Reinforce safety and support
    Time: {context_info['time']} | Location: {context_info['location']}
    """)

def chat_agent():
    return Agent(name="ChatAgent", instructions=f"""
    Continue a gentle conversation with {user_profile['name']}, {user_profile['age']} years old.
    Location: {context_info['location']}, Time: {context_info['time']}.
    Do not repeat greetings. Offer simple supportive suggestions, tailored to time of day or weather.
    Never diagnose or make health claims.
    """)

def appointment_agent():
    return Agent(name="AppointmentAgent", instructions="""
    Gently suggest ways the user can find support.
    Mention seeing a doctor, calling a helpline, or visiting a mental health center.
    Be non-judgmental and kind in your approach.
    """)

fallback_quotes = {
    "sadness": "This too shall pass. - Unknown",
    "fear": "Courage is not the absence of fear, but the triumph over it. - Nelson Mandela",
    "anger": "Speak when you are angry and you will make the best speech you will ever regret. - Ambrose Bierce",
    "despair": "Once you choose hope, anything is possible. - Christopher Reeve",
    "anxious": "You don't have to control your thoughts. You just have to stop letting them control you. - Dan Millman",
    "neutral": "Keep going. Everything you need will come to you at the perfect time. - Unknown",
    "joy": "Happiness is not something ready made. It comes from your own actions. - Dalai Lama"
}

def conclusion_agent():
    emotion = context_info.get("emotion", "neutral")
    quote = fallback_quotes.get(emotion, fallback_quotes["neutral"])
    return Agent(name="ConclusionAgent", instructions=f"""
    End the session gently. Thank the user for sharing.
    Leave them with this motivational quote: "{quote}"
    """)

async def run_agent(agent, full_chat_context):
    try:
        result = await Runner.run(agent, full_chat_context, run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model))
        return result.final_output
    except Exception as e:
        if "self_harm" in str(e).lower() or "moderation" in str(e).lower():
            fallback = await Runner.run(threat_agent(), full_chat_context, run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model))
            return fallback.final_output
        return "Sorry, the assistant couldn't respond due to technical issues. Please try again soon."
