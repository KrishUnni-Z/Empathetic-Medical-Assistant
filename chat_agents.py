from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    return Agent(
        name="WelcomeAgent",
        instructions=f"""
        You are a kind assistant helping {user_profile['name']} ({user_profile['age']}, {user_profile['gender']}).
        It's currently {context_info['time']} in {context_info['location']}.
        Greet the user warmly, offer comfort, and mention it's okay to seek help.
        Include wellness tips like rest, hydration, and peace of mind.
        """.strip()
    )

def threat_agent(user_input=""):
    return Agent(
        name="ThreatAgent",
        instructions=f"""
        The user has shown emotional distress: {context_info.get('emotion', 'unknown')}.
        You are a non-judgmental, emotionally aware assistant.
        Do not give diagnoses. Urge them to seek support from loved ones or emergency lines.
        Time: {context_info['time']}, Location: {context_info['location']}
        """
    )

def chat_agent():
    return Agent(
        name="ChatAgent",
        instructions=f"""
        Continue an ongoing conversation with {user_profile['name']} ({user_profile['age']}, {user_profile['gender']}).
        Use context: {context_info['location']}, {context_info['time']} to offer comforting advice or health tips.
        Do not repeat greetings. Avoid diagnosis.
        """
    )

def appointment_agent():
    return Agent(
        name="AppointmentAgent",
        instructions="""
        Gently guide the user toward getting medical support nearby.
        Mention helplines, clinics, or doctors if appropriate.
        Do not pressure them. Just be helpful.
        """
    )

def conclusion_agent():
    quotes = {
        "sadness": "This too shall pass.",
        "fear": "Courage is not the absence of fear, but the triumph over it. - Mandela",
        "anger": "Speak when you are angry and you will make the best speech you will ever regret.",
        "despair": "Once you choose hope, anything is possible.",
        "anxious": "You don't have to control your thoughts. Just stop letting them control you.",
        "neutral": "Keep going. Everything you need will come to you at the perfect time.",
        "joy": "Happiness comes from your own actions. - Dalai Lama"
    }
    quote = quotes.get(context_info.get("emotion", "neutral"), quotes["neutral"])
    return Agent(
        name="ConclusionAgent",
        instructions=f"Thank the user. Give them this quote to leave them inspired: '{quote}'"
    )

async def run_agent(agent, context):
   response = await Runner.run(agent, context, run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model))
   return response.final_output
    
