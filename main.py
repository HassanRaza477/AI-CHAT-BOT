import requests
import json
import streamlit as st

userdata = {
    "OPENROUTER_API_KEY": "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"
}

OPENROUTER_API_KEY = userdata.get("OPENROUTER_API_KEY")

MODEL_ID = "deepseek/deepseek-r1-0528:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}
st.set_page_config(page_title="🧠 UV Chatbot", layout="centered")
st.title("🤖 HR Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("💬 Type your message...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "system", "content": "You are a helpful assistant."}]
        + st.session_state.chat_history
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.session_state.chat_history.append({"role": "assistant", "content": f"❌ Error: {e}"})

# Display messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
