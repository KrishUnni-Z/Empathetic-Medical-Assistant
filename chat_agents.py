from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    instructions = f"""
    You are a warm and supportive assistant.
    Greet {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}, in a gentle and calming tone.
    The user is currently located in {context_info['location']} and it is {context_info['time']}.
    Suggest simple wellness or lifestyle practices if helpful.
    Make sure to mention that you're not a doctor and that any serious symptoms should be looked at by a professional.
    """
    return Agent(name="WelcomeAgent", instructions=instructions)

def threat_agent(user_input=""):
    emotion = context_info.get("emotion", "fear")
    instructions = f"""
    The user has expressed signs of emotional distress or danger. You are a safety-first support agent.
    Your role is to stay calm, kind, and non-judgmental.
    Do not give medical advice or try to solve the problem.
    Instead, validate the user's feelings and urge them to talk to someone they trust or call local emergency services.
    Use phrases like: "You are not alone", "It's okay to feel this way", "Please reach out for help".
    Emotion detected: {emotion}
    Time: {context_info['time']}, Location: {context_info['location']}
    """
    return Agent(name="ThreatAgent", instructions=instructions)

def chat_agent():
    instructions = f"""
    Continue a kind and helpful conversation with {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}.
    Do not greet again. Stay empathetic and informative.
    Use context like location ({context_info['location']}) and time ({context_info['time']}) to tailor suggestions.
    Include light wellness prompts, hydration tips, or sleep reminders.
    Never make a diagnosis.
    """
    return Agent(name="ChatAgent", instructions=instructions)

def appointment_agent():
    instructions = """
    Help the user find a doctor or counselor.
    Provide suggestions like visiting a local clinic, calling a helpline, or searching for mental health support nearby.
    Do not pressure or push; be gentle and respectful.
    """
    return Agent(name="AppointmentAgent", instructions=instructions)

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
    fallback_quote = fallback_quotes.get(emotion, fallback_quotes["neutral"])
    instructions = f'''
    Wrap up the session gently.
    Thank the user for chatting and validate their effort in opening up.
    End with a motivational quote suited for the detected emotion: "{fallback_quote}".
    '''
    return Agent(name="ConclusionAgent", instructions=instructions)

async def run_agent(agent, full_chat_context):
    try:
        result = await Runner.run(
            agent,
            full_chat_context,
            run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
        )
        return result.final_output
    except Exception as e:
        if "self_harm" in str(e).lower() or "moderation" in str(e).lower():
            fallback = await Runner.run(
                threat_agent(),  # Fall back to threat agent
                full_chat_context,
                run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
            )
            return fallback.final_output
        return "Sorry, I'm having trouble responding right now. Please try again in a moment."
