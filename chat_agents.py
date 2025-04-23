from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile

def welcome_agent():
    return Agent(
        name="WelcomeAgent",
        instructions=f"""
        You are a kind assistant helping {user_profile['name']} ({user_profile['age']}, {user_profile['gender']}).
        It's currently {context_info['time']} in {context_info['location']}.
        Greet the user warmly and offer comfort and health tips.
        """
    )

def threat_agent(reason=""):
    return Agent(
        name="ThreatAgent",
        instructions=f"""
        The user is experiencing distress related to: {reason}.
        You are a calm, supportive assistant. Do not give diagnoses.
        Urge the user to contact trusted people, or call support lines.
        Time: {context_info['time']}, Location: {context_info['location']}
        """
    )

def chat_agent():
    return Agent(
        name="ChatAgent",
        instructions=f"""
        Continue chatting with {user_profile['name']} ({user_profile['age']}, {user_profile['gender']}).
        Consider time: {context_info['time']} and location: {context_info['location']}.
        Offer friendly health tips, not diagnosis. Avoid repeating greetings.
        """
    )

def appointment_agent(emotion="neutral"):
    tips = {
        "despair": "You can call Lifeline Australia at 13 11 14 or visit beyondblue.org.au.",
        "anxious": "You might find MindSpot or Head to Health useful for anxiety.",
        "sadness": "You are not alone. Consider talking to a friend or calling Lifeline (13 11 14).",
        "fear": "You're safe. If this fear persists, you can seek calm guidance through a GP.",
        "anger": "Try to breathe deeply. Anger support groups or a psychologist might help.",
        "suicidal": "Please call 000 or Lifeline (13 11 14) immediately. You matter.",
        "neutral": "If you're unsure, you can always start with a free support line like Lifeline or Beyond Blue.",
        "joy": "Wonderful to hear! Remember to check in with others who might need support too."
    }
    tip = tips.get(emotion, tips["neutral"])
    return Agent(
        name="AppointmentAgent",
        instructions=f"""
        Offer mental health support guidance for someone feeling {emotion}.
        Suggest Australian resources, hotlines, or websites.
        Specific support: {tip}
        """
    )

def conclusion_agent():
    quotes = {
        "sadness": "This too shall pass.",
        "fear": "Courage is not the absence of fear, but the triumph over it.",
        "anger": "Speak when you are angry and you will make the best speech you will ever regret.",
        "despair": "Once you choose hope, anything is possible.",
        "anxious": "You don't have to control your thoughts. Just stop letting them control you.",
        "neutral": "Keep going. Everything you need will come to you at the perfect time.",
        "joy": "Happiness comes from your own actions."
    }
    quote = quotes.get(context_info.get("emotion", "neutral"), quotes["neutral"])
    return Agent(
        name="ConclusionAgent",
        instructions=f"Thank the user for the chat and share this quote: '{quote}'"
    )

async def run_agent(agent, context):
    response = await Runner.run(agent, context, run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model))
    return response.final_output
