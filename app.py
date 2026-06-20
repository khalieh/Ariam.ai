import streamlit as st
import os
from google import genai
from google.genai import types

st.title("🤖 Chat with Ariam")
st.write("Welcome to Ariam's independent home on the web!")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    st.error("Please add your secure API key to Streamlit Secrets.")

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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction="Your name is Ariam. You are a helpful, friendly, and smart native AI assistant.",
            ),
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Ariam is having trouble connecting. Double check your Secrets vault!")
