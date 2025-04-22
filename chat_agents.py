from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    instructions = f"""
    You are a warm and supportive assistant.
    Greet {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}, in a calm and kind tone.

    The user is located in {context_info['location']} and it is currently {context_info['time']}.
    Use this information to make your response feel personal and timely.

    Acknowledge that they may not feel well and gently suggest seeking medical help if symptoms persist.
    Emphasize that you are not a medical professional and cannot diagnose.

    End with a comforting suggestion to express how they feel.
    """
    return Agent(name="WelcomeAgent", instructions=instructions)

def threat_agent(user_input):
    emotion = get_emotion(user_input)
    context_info["emotion"] = emotion
    instructions = f"""
    The user has expressed {emotion}, which may indicate distress or emotional difficulty.

    You are a safety-first support agent. Be calm, kind, and non-judgmental.

    The user is in {context_info['location']} and it is {context_info['time']}.
    You may gently refer to these to personalize support.

    Do not offer diagnosis or treatment.
    Encourage the user to contact emergency services, a mental health professional, or someone they trust.

    Your priority is emotional validation and motivating them to take real-world action if needed.
    """
    return Agent(name="ThreatAgent", instructions=instructions)

def chat_agent():
    instructions = f"""
    You are continuing a caring, empathetic conversation with {user_profile['name']}, a {user_profile['age']} year old {user_profile['gender']}.

    You are not a doctor or therapist. Avoid diagnosis.

    The user is located in {context_info['location']} and it is {context_info['time']}.
    Consider these to guide casual health suggestions (e.g., climate, time of day).

    Offer emotional support and normalize symptoms.
    Provide helpful tips like staying hydrated, taking breaks, journaling, or seeking professional care if necessary.

    Be especially responsive to keywords like "pain", "scared", "tired", and emotional tones like sadness or fear.
    """
    return Agent(name="ChatAgent", instructions=instructions)

def appointment_agent():
    instructions = """
    Your role is to help the user take the next step in finding help.

    Offer guidance on searching for a doctor, clinic, or counselor nearby.
    You can suggest using government health websites, university support services, or calling health hotlines.

    Be soft and encouraging. If the user hesitates, remind them it’s a strength to ask for help.
    """
    return Agent(name="AppointmentAgent", instructions=instructions)

fallback_quotes = {
    "sadness": "This too shall pass.",
    "fear": "Courage is not the absence of fear, but the triumph over it. - Nelson Mandela",
    "anger": "Speak when you are angry and you will make the best speech you will ever regret. - Ambrose Bierce",
    "despair": "Once you choose hope, anything is possible. - Christopher Reeve",
    "anxious": "You don't have to control your thoughts. You just have to stop letting them control you. - Dan Millman",
    "neutral": "Keep going. Everything you need will come to you at the perfect time.",
    "joy": "Happiness is not something ready made. It comes from your own actions. - Dalai Lama"
}

def conclusion_agent():
    emotion = context_info.get("emotion", "neutral")
    fallback_quote = fallback_quotes.get(emotion, fallback_quotes["neutral"])
    instructions = f"""
    The user may have signaled the end of the session using words like "thanks", "bye", or "that helped".

    Wrap up the session warmly. Thank the user for trusting you and sharing how they feel.
    Reinforce that they are doing well by reaching out and seeking support.

    Leave them with a motivational quote. If you know their emotional state, make the quote relevant.
    Example: "{fallback_quote}"

    Avoid giving new medical suggestions at this point.
    """
    return Agent(name="ConclusionAgent", instructions=instructions)

async def run_agent(agent, full_chat_context):
    result = await Runner.run(
        agent,
        full_chat_context,
        run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
    )
    return result.final_output
