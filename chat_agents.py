from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    instructions = f"""
    You are a warm and supportive assistant.
    Greet {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}, in a gentle and calming tone.

    The user is currently located in {context_info['location']} and it is {context_info['time']}.
    Use this context if it helps ground your advice or comfort.

    Let the user know they are in a private space and free to express themselves.
    End with a soft, helpful suggestion that’s comforting based on what they mentioned.
    """
    return Agent(name="WelcomeAgent", instructions=instructions)

def threat_agent(user_input):
    emotion = get_emotion(user_input)
    context_info["emotion"] = emotion
    instructions = f"""
    The user has expressed {emotion} and may be in distress.
    You are a safety-first support agent and must be calm, reassuring, and non-judgmental.

    The user is located in {context_info['location']} and it is currently {context_info['time']}.
    You may refer to their environment gently if it helps.

    Do not diagnose or give advice — instead, validate their feelings, provide support, and suggest reaching out to professionals.
    """
    return Agent(name="ThreatAgent", instructions=instructions)

def chat_agent():
    instructions = f"""
    You are continuing a kind and empathetic conversation with {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}.

    Do not greet the user again. Respond naturally in a flowing tone as if the conversation is ongoing.

    The user is in {context_info['location']} and it is currently {context_info['time']}.
    Use this to tailor your suggestions (e.g., climate-triggered symptoms, sleep, hydration, light).

    Stay emotionally supportive. Suggest relevant, simple comfort actions, but don’t be repetitive or robotic.
    """
    return Agent(name="ChatAgent", instructions=instructions)

def appointment_agent():
    instructions = """
    Help the user find appropriate support. Offer brief guidance on how to find a doctor or counselor nearby.

    Do not pressure the user — be supportive and understanding.
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
    instructions = f"""
    Gently wrap up the session. Thank the user for sharing and validate their openness.

    End with an emotionally appropriate inspirational quote for {emotion}, or use:
    "{fallback_quote}"
    """
    return Agent(name="ConclusionAgent", instructions=instructions)

async def run_agent(agent, full_chat_context):
    result = await Runner.run(
        agent,
        full_chat_context,
        run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
    )
    return result.final_output
