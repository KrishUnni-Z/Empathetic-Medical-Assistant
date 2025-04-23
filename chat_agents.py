from agents import Agent, Runner, RunConfig
from config import MODEL_PROVIDER, model
from core import context_info, user_profile, get_emotion

def welcome_agent():
    return Agent(
        name="WelcomeAgent",
        instructions=f"""
        You are a supportive assistant welcoming {user_profile['name']}, aged {user_profile['age']}, identifying as {user_profile['gender']}.
        The user is currently in {context_info['location']} at {context_info['time']}.
        Use this context gently to offer comfort. End with a suggestion to continue the conversation.
        """
    )

def threat_agent(user_input):
    emotion = get_emotion(user_input)
    context_info["emotion"] = emotion
    return Agent(
        name="ThreatAgent",
        instructions=f"""
        The user expressed signs of distress (emotion: {emotion}).
        Offer validation and calm reassurance. Encourage reaching out to trusted support.
        Avoid diagnosis or solutions. Emphasize emotional safety and gentle care.
        """
    )

def chat_agent():
    return Agent(
        name="ChatAgent",
        instructions=f"""
        You are chatting with {user_profile['name']}, aged {user_profile['age']}, from {context_info['location']} at {context_info['time']}.
        Continue the conversation empathetically. Avoid repeating past suggestions.
        Provide relevant comfort actions such as rest, hydration, or calm breathing.
        """
    )

def appointment_agent():
    return Agent(
        name="AppointmentAgent",
        instructions="""
        Help the user find a nearby healthcare provider or counselor.
        Gently suggest online directories, clinics, or help lines. Avoid pressure.
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
        Thank the user for sharing. Offer an uplifting and safe farewell.
        Include this quote: "{quote}"
        Encourage them to return any time for more support.
        '''
    )

def moderation_fallback_agent(reason="moderation"):
    return Agent(
        name="FallbackSafetyAgent",
        instructions=f"""
        The user's message could not be processed due to {reason}-related filtering.
        Respond with a calm and caring tone. Emphasize that the assistant is here to listen and offer comfort.
        Avoid triggering content or deep analysis. Let them know support is always available.
        """
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
        error_str = str(e).lower()
        # Check moderation tags
        flagged_tags = ["self_harm", "violence", "sexual", "hate", "moderation"]
        reason = next((tag for tag in flagged_tags if tag in error_str), "moderation")

        # Use fallback safety agent
        fallback = moderation_fallback_agent(reason)
        fallback_result = await Runner.run(
            fallback,
            "The original message was filtered. Offer supportive fallback.",
            run_config=RunConfig(model_provider=MODEL_PROVIDER, model=model)
        )
        return fallback_result.final_output
