import streamlit as st
import asyncio
import os
from core import (
    get_time, get_location, get_emotion, load_profile, save_profile,
    user_profile, context_info
)
from chat_agents import (
    welcome_agent, threat_agent, chat_agent,
    appointment_agent, conclusion_agent, run_agent
)

# ----------------- Setup -----------------
st.set_page_config(page_title="Empathetic Medical Assistant", layout="wide")
load_profile()

# ----------------- UI Styling -----------------
st.markdown(
    '''
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stChatInputContainer textarea {
        min-height: 70px !important;
        font-size: 16px !important;
        padding: 0.75rem !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# ----------------- Session -----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "started" not in st.session_state:
    st.session_state.started = False

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown("### Profile")

    # Theme toggle
    theme_choice = st.radio("Theme", ["Dark", "Light"], index=0)
    if "theme" not in st.session_state:
        st.session_state.theme = theme_choice

    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        config = f"""
[theme]
base="{theme_choice.lower()}"
primaryColor="#FF4B4B"
backgroundColor="{ '#FFFFFF' if theme_choice == 'Light' else '#0E1117' }"
secondaryBackgroundColor="{ '#F0F2F6' if theme_choice == 'Light' else '#262730' }"
textColor="{ '#000000' if theme_choice == 'Light' else '#FAFAFA' }"
        os.makedirs(".streamlit", exist_ok=True)
        with open(".streamlit/config.toml", "w") as f:
            f.write(config)
        st.success("✅ Theme updated! Please **refresh your browser tab** (Ctrl + R) to apply.")
        st.stop()

    # Reset / clear buttons
    if st.button("Reset Profile"):
        if os.path.exists("user_profile.txt"):
            os.remove("user_profile.txt")
        user_profile["name"] = ""
        user_profile["age"] = ""
        user_profile["gender"] = ""
        st.session_state.started = False
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    # Profile form
    if not st.session_state.started:
        with st.form("profile_form"):
            name = st.text_input("Your Name", value=user_profile["name"])
            age = st.number_input("Your Age", min_value=1, max_value=120, step=1)
            gender = st.selectbox(
                "Gender", ["Male", "Female", "Other"],
                index=["Male", "Female", "Other"].index(user_profile["gender"]) if user_profile["gender"] else 0
            )
            submitted = st.form_submit_button("Start")

        if submitted:
            user_profile["name"] = name
            user_profile["age"] = str(age)
            user_profile["gender"] = gender
            context_info["time"] = get_time()
            context_info["location"] = get_location()
            save_profile()
            st.session_state.started = True
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown(f"- **Name:** {user_profile['name']}")
        st.markdown(f"- **Age:** {user_profile['age']}")
        st.markdown(f"- **Gender:** {user_profile['gender']}")

# ----------------- Main Interface -----------------
st.title("Empathetic Medical Assistant")
st.markdown("*This assistant is powered by AI and is not a substitute for professional medical advice.*")

if st.session_state.get("started", False):
    if len(st.session_state.chat_history) == 0:
        st.markdown(f"👋 Welcome, **{user_profile['name']}**! Type how you're feeling to begin the conversation.")

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(f"<div style='font-size: 15px; max-width: 100%;'>{message}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Type your message:")

    if user_input:
        emotion = get_emotion(user_input)
        context_info["emotion"] = emotion

        agent = (
            threat_agent(user_input)
            if len(st.session_state.chat_history) == 0 and emotion in ["despair", "suicidal", "fear", "anger", "sadness"]
            else welcome_agent()
            if len(st.session_state.chat_history) == 0
            else chat_agent()
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        chat_context = ""
        for role, msg in st.session_state.chat_history[-10:]:
            chat_context += f"{'User' if role == 'user' else 'Assistant'}: {msg}\n"
        chat_context += f"User: {user_input}"

        reply = asyncio.run(run_agent(agent, chat_context))

        with st.chat_message("bot"):
            st.markdown(f"<div style='font-size: 15px; max-width: 100%;'>{reply}</div>", unsafe_allow_html=True)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", reply))

    # ----------------- Get Support -----------------
    if st.button("Get Support"):
        with st.chat_message("bot"):
            st.write("Let me help you with that.")
            support_reply = asyncio.run(run_agent(appointment_agent(), ""))
            st.markdown(f"<div style='font-size: 15px'>{support_reply}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append(("bot", support_reply))

        with st.chat_message("bot"):
            st.markdown("Would you like to end this session with a final message, or continue talking?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🛑 End Chat"):
                    final_reply = asyncio.run(run_agent(conclusion_agent(), ""))
                    with st.chat_message("bot"):
                        st.markdown(f"<div style='font-size: 15px'>{final_reply}</div>", unsafe_allow_html=True)
                    st.session_state.chat_history.append(("bot", final_reply))
            with col2:
                if st.button("🔁 Continue Talking"):
                    st.rerun()
