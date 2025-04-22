import streamlit as st
import asyncio
import os
import streamlit.components.v1 as components
from core import (
    get_time, get_emotion, load_profile, save_profile,
    user_profile, context_info
)
from chat_agents import (
    welcome_agent, threat_agent, chat_agent,
    appointment_agent, conclusion_agent, run_agent
)

st.set_page_config(page_title="Empathetic Medical Assistant", layout="wide")
load_profile()

st.markdown('''
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
''', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "started" not in st.session_state:
    st.session_state.started = False

# --- Inject JS to try browser location ---
components.html("""
<script>
navigator.geolocation.getCurrentPosition(
    function(pos) {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const loc = lat.toFixed(2) + "," + lon.toFixed(2);
        const input = window.parent.document.getElementById("location-input");
        if (input) {
            input.value = loc;
            input.dispatchEvent(new Event("input", { bubbles: true }));
        }
    },
    function(err) {
        console.log("Geolocation error:", err.message);
    }
);
</script>
<input type="hidden" id="location-input">
""", height=0)

# --- Sidebar profile form ---
with st.sidebar:
    st.markdown("### Profile")

    if st.button("Reset Profile"):
        if os.path.exists("user_profile.txt"):
            os.remove("user_profile.txt")
        user_profile.update({"name": "", "age": "", "gender": "", "location": ""})
        st.session_state.started = False
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if not st.session_state.started:
        with st.form("profile_form"):
            name = st.text_input("Your Name", value=user_profile["name"])
            age = st.number_input("Your Age", min_value=1, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                  index=["Male", "Female", "Other"].index(user_profile["gender"]) if user_profile["gender"] else 0)

            js_location = st.text_input("Detected Location (auto)", key="location-input")
            manual_location = st.text_input("Or enter your location manually")

            final_location = js_location if js_location else manual_location

            submitted = st.form_submit_button("Start")

        if submitted:
            user_profile.update({
                "name": name,
                "age": str(age),
                "gender": gender,
                "location": final_location if final_location else "Not provided"
            })
            context_info["time"] = get_time()
            context_info["location"] = user_profile["location"]
            save_profile()
            st.session_state.started = True
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown(f"- Name: {user_profile['name']}")
        st.markdown(f"- Age: {user_profile['age']}")
        st.markdown(f"- Gender: {user_profile['gender']}")
        if user_profile["location"]:
            st.markdown(f"- Location: {user_profile['location']}")

# --- Main UI ---
st.title("Empathetic Medical Assistant")
st.markdown("*This assistant is powered by AI and is not a substitute for professional medical advice.*")

# Session context
st.markdown("#### Session Context")
st.markdown(f"**Location:** {user_profile['location'] or 'Not provided'}")
st.markdown(f"**Local Time:** {context_info.get('time') or 'Unavailable'}")

components.html("""
<div style='font-size:18px; margin-top: 10px;'>
    <b>Live Clock:</b> <span id='clock'></span>
</div>
<script>
    function updateClock() {
        const now = new Date();
        document.getElementById('clock').textContent = now.toLocaleTimeString();
    }
    setInterval(updateClock, 1000);
    updateClock();
</script>
""", height=40)

# --- Chatbot Interface ---
if st.session_state.started:
    if len(st.session_state.chat_history) == 0:
        st.markdown(f"Welcome, {user_profile['name']}! Type how you're feeling to begin the conversation.")

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

        chat_context = f"User: {user_input}"
        try:
            reply = asyncio.run(run_agent(agent, chat_context))
        except Exception:
            reply = "I'm sorry, the assistant is currently busy or rate-limited. Please try again shortly."

        with st.chat_message("bot"):
            st.markdown(f"<div style='font-size: 15px'>{reply}</div>", unsafe_allow_html=True)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", reply))

    if st.button("Get Support"):
        with st.chat_message("bot"):
            st.write("Let me help you with that.")
            support_reply = asyncio.run(run_agent(appointment_agent(), ""))
            st.markdown(f"<div style='font-size: 15px'>{support_reply}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append(("bot", support_reply))

        st.markdown("Would you like to end this session with a final message, or continue talking?")
        if st.button("End Chat"):
            with st.chat_message("bot"):
                final_reply = asyncio.run(run_agent(conclusion_agent(), ""))
                st.markdown(f"<div style='font-size: 15px'>{final_reply}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append(("bot", final_reply))
            st.session_state.started = False
        elif st.button("Continue Talking"):
            st.rerun()
