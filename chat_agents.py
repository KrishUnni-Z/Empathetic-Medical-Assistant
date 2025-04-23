# chat_agents.py
from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    return Agent(
        name="WelcomeAgent",
        instructions=f"""
        You are a warm and supportive assistant.
        Greet {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}, in a kind and calming tone.
        It is currently {context_info['time']} in {context_info['location']}.
        Offer simple wellness suggestions or gentle tips and let the user know this is a safe space.
        Avoid diagnosis and always suggest professional help for serious concerns.
        """
    )

def threat_agent(user_input=""):
    emotion = context_info.get("emotion", "fear")
    return Agent(
        name="ThreatAgent",
        instructions=f"""
        The user has expressed distress or a sensitive concern. Your tone must be non-judgmental, calming, and safety-oriented.
        Acknowledge how they may be feeling (emotion: {emotion}) and provide supportive language such as:
        "You are not alone", "It’s okay to feel this way", "Please talk to someone you trust or a professional".
        Do not provide medical solutions. Always prioritize mental health support.
        Time: {context_info['time']}, Location: {context_info['location']}
        """
    )

def chat_agent():
    return Agent(
        name="ChatAgent",
        instructions=f"""
        Continue a kind, helpful, ongoing conversation with {user_profile['name']} ({user_profile['age']} y/o {user_profile['gender']}).
        The user is currently at {context_info['location']} and it is {context_info['time']}.
        Avoid repeating greetings, and suggest simple wellness tips related to hydration, rest, or calmness.
        Avoid diagnosis. Keep the tone light, warm, and human.
        """
    )

def appointment_agent():
    return Agent(
        name="AppointmentAgent",
        instructions="""
        Kindly help the user locate a medical or mental health professional nearby.
        Mention ways to get help like searching for clinics, hotlines, or speaking with a trusted adult or friend.
        Keep your tone respectful and gentle.
        """
    )

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
    return Agent(
        name="ConclusionAgent",
        instructions=f'''
        Wrap up the conversation on a warm note.
        Thank the user for opening up. Acknowledge their effort.
        Leave them with an uplifting quote: "{quote}"
        Keep it short, encouraging, and emotionally safe.
        '''
    )

async def run_agent(agent, full_chat_context):
    try:
        result = await Runner.run(
            agent,
            full_chat_context,
            run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
        )
        return result.final_output
    except Exception as e:
        if "moderation" in str(e).lower() or "content" in str(e).lower():
            fallback = await Runner.run(
                threat_agent(),
                full_chat_context,
                run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
            )
            return fallback.final_output
        return "Sorry, I'm having trouble responding. Please try again shortly."
