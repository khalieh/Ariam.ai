import streamlit as st
import google.generativeai as genai

st.title("🤖 Chat with Ariam")
st.write("Welcome to Ariam's official home! Type a message below to talk to her.")

# Safe connection to read your background key
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Modern authentication that supports AQ. key formats
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Missing API Key! Please add your key to Streamlit Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Say something to Ariam..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Your name is Ariam. You are a helpful, friendly, and smart native AI assistant."
        )
        response = model.generate_content(user_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Connection Error: Please verify that your Streamlit Secrets vault has the correct key.")
