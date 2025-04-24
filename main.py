import streamlit as st
import requests
from datetime import datetime

# --- CONFIG ---
API_URL = "http://localhost:3000/api/v1/prediction/1e1b8c66-66e9-4eb5-a42a-c8fadc6d3a88"
st.set_page_config(page_title="ContextIQ", layout="centered", page_icon="🧠")

# --- STYLING ---
st.markdown("""
    <style>
        .main { background-color: #fafafa; }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            padding: 0.6em;
            font-size: 16px;
        }
        .stButton button {
            border-radius: 8px;
            background-color: #4a90e2;
            color: white;
            font-weight: 600;
        }
        .chat-bubble {
            padding: 0.8em;
            margin: 0.5em 0;
            border-radius: 1em;
            max-width: 90%;
        }
        .user-bubble {
            background-color: #d6ecff;
            align-self: flex-end;
        }
        .bot-bubble {
            background-color: #eeeeee;
            align-self: flex-start;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712040.png", width=100)  # Optional logo
    st.title("🧠 ContextIQ")
    st.write("Fetch contextual knowledge from your uploaded documents via Flowise AI.")
    st.markdown("---")
    st.caption("Powered by Flowise on Render")

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- UI HEADER ---
st.title("Ask a Question from Your Documents")

# --- QUESTION INPUT ---
question = st.text_input("Your question", placeholder="e.g., What is the payment clause in the contract?")
ask = st.button("Ask")

# --- ASK & DISPLAY CHAT ---
if ask and question.strip():
    st.session_state.chat_history.append(("user", question))

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={"question": question}
            )
            if response.ok:
                answer = response.json().get("text", "No answer returned.")
                st.session_state.chat_history.append(("bot", answer))
            else:
                st.session_state.chat_history.append(("bot", f"❌ Error {response.status_code}: {response.text}"))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f"❌ Request failed: {e}"))

# --- DISPLAY CHAT BUBBLES ---
for sender, message in st.session_state.chat_history:
    bubble_class = "user-bubble" if sender == "user" else "bot-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{message}</div>", unsafe_allow_html=True)

# --- OPTIONAL FEEDBACK ---
st.markdown("---")
st.caption("❓ Found a mistake? [Submit feedback](https://forms.gle/your-feedback-form)")
