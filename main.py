import os
import requests
import json
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Constants
MODEL_ID = "deepseek/deepseek-r1-0528:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Set Streamlit page config
st.set_page_config(page_title="🧠 UV Chatbot", layout="centered")
st.title("🤖 HR Chatbot")

# Sidebar controls
st.sidebar.title("HR Chatbot")

if st.sidebar.button("🆕 New Chat"):
    st.session_state.chat_history = []

# Save chat history as .txt
if st.session_state.get("chat_history"):
    chat_text = "\n\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in st.session_state.chat_history
    ])
    st.sidebar.download_button(
        label="💾 Save Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Default system prompt
system_prompt = "You are Hoor, a friendly and witty chatbot that helps users casually."

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Get user input
user_input = st.chat_input("💬 Type your message...")

# Show previous chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user message
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Thinking...")

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "system", "content": system_prompt}]
        + st.session_state.chat_history
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Error: {e}"

    placeholder.markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
