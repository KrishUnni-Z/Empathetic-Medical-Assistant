import streamlit as st
import asyncio
import os
import json
from core import (
    get_time, get_location, get_emotion, load_profile, save_profile,
    user_profile, context_info
)
from chat_agents import (
    welcome_agent, threat_agent, chat_agent,
    appointment_agent, conclusion_agent, run_agent
)
from agents import RunConfig, Runner
from config import MODEL_PROVIDER, model

st.set_page_config(page_title="Empathetic Medical Assistant", layout="wide")
load_profile()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "started" not in st.session_state:
    st.session_state.started = False
if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

detected_location = get_location()
detected_time = get_time()

with st.sidebar:
    st.markdown("### Profile")

    if st.button("Reset Profile"):
        if os.path.exists("user_profile.txt"):
            os.remove("user_profile.txt")
        user_profile.update({"name": "", "age": "", "gender": ""})
        st.session_state.started = False
        st.session_state.chat_ended = False
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if not st.session_state.started:
        with st.form("profile_form"):
            name = st.text_input("Your Name", value=user_profile["name"])
            age = st.number_input("Your Age", min_value=1, max_value=120,
                                  value=int(user_profile["age"]) if user_profile["age"].isdigit() else 25)
            gender_options = ["Select", "Male", "Female", "Other"]
            gender = st.selectbox("Gender", gender_options,
                                  index=gender_options.index(user_profile["gender"]) if user_profile["gender"] in gender_options else 0)
            manual_location = st.text_input("Your Location", value=detected_location)
            manual_time = st.text_input("Current Time", value=detected_time)
            submitted = st.form_submit_button("Start")

        if submitted:
            if not name or gender == "Select":
                st.warning("Please complete all profile fields.")
            else:
                user_profile.update({"name": name, "age": str(age), "gender": gender})
                context_info["location"] = manual_location
                context_info["time"] = manual_time
                save_profile()
                st.session_state.started = True
                st.session_state.chat_ended = False
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.markdown(f"- **Name:** {user_profile['name']}")
        st.markdown(f"- **Age:** {user_profile['age']}")
        st.markdown(f"- **Gender:** {user_profile['gender']}")
        st.markdown(f"- **Location:** {context_info['location'] or 'Unknown'}")
        st.markdown(f"- **Time:** {context_info['time'] or 'Unavailable'}")

st.title("Empathetic Medical Assistant")
st.markdown("*AI-powered assistant. Not a substitute for professional medical advice.*")

def get_safe_moderation_context(reason):
    return f"The user may need help related to {reason}. Please respond with a calm and supportive message urging them to talk to someone or seek help."

if st.session_state.get("started", False):
    if len(st.session_state.chat_history) == 0:
        st.markdown(f"👋 Welcome, **{user_profile['name']}**! How are you feeling today?")

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(f"<div style='font-size: 15px'>{message}</div>", unsafe_allow_html=True)

    if not st.session_state.get("chat_ended", False):
        user_input = st.chat_input("Type your message:")
        if user_input:
            emotion = get_emotion(user_input)
            context_info["emotion"] = emotion

            high_risk_emotions = ["despair", "suicidal", "fear", "anger", "sadness"]
            if emotion in high_risk_emotions:
                agent = threat_agent(emotion)
            elif len(st.session_state.chat_history) == 0:
                agent = welcome_agent()
            else:
                agent = chat_agent()

            with st.chat_message("user"):
                st.markdown(user_input)

            chat_context = "\n".join(
                f"{'User' if role == 'user' else 'Assistant'}: {msg}"
                for role, msg in st.session_state.chat_history[-10:]
            ) + f"\nUser: {user_input}"

            try:
                reply = asyncio.run(run_agent(agent, chat_context))

            except Exception as e:
                reason = "moderation_flagged"
                try:
                    error_str = str(e)
                    if "content_filter_result" in error_str:
                        json_part = error_str.split("{", 1)[1]
                        json_str = "{" + json_part.replace("'", '"')
                        error_data = json.loads(json_str)
                        filters = error_data["error"]["innererror"]["content_filter_result"]
                        for category, result in filters.items():
                            if result.get("filtered"):
                                reason = category
                                break
                except Exception:
                    reason = "moderation_unknown"

                with st.chat_message("bot"):
                    st.warning("Your message triggered safety moderation. You're not alone — here's something that might help.")

                fallback_agent = threat_agent(f"Azure moderation triggered: {reason}")
                safe_context = get_safe_moderation_context(reason)
                reply = asyncio.run(run_agent(fallback_agent, safe_context))

            with st.chat_message("bot"):
                st.markdown(f"<div style='font-size: 15px'>{reply}</div>", unsafe_allow_html=True)

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", reply))
    else:
        st.info("The chat has ended. Please reset your profile to begin again.")

    if st.button("📞 Get Support"):
        support_reply = asyncio.run(run_agent(appointment_agent(), ""))
        with st.chat_message("bot"):
            st.markdown(f"<div style='font-size: 15px'>{support_reply}</div>", unsafe_allow_html=True)
        st.session_state.chat_history.append(("bot", support_reply))

    if st.button("🛑 End Chat"):
        final_reply = asyncio.run(run_agent(conclusion_agent(), ""))
        with st.chat_message("bot"):
            st.markdown(f"<div style='font-size: 15px'>{final_reply}</div>", unsafe_allow_html=True)
        st.session_state.chat_history.append(("bot", final_reply))
        st.session_state.chat_ended = True
