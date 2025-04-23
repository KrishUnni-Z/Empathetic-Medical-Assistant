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

def appointment_agent():
    return Agent(
        name="AppointmentAgent",
        instructions=f"""
        The user may need mental health support.
        Their location is: {context_info['location']}.
        Provide region-specific or country-specific support services, such as:
        - Mental health hotlines
        - Local clinics
        - Online therapy services
        If the location is missing or unknown, recommend global services like WHO, Befrienders, or TalkLife.
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
