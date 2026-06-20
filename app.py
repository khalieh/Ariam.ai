import streamlit as st
import google.generativeai as genai

# 1. Title of your webpage
st.title("🤖 Chat with Ariam")
st.write("Welcome to Ariam's official home on the internet! Type a message below to start talking.")

# 2. Add your secret API key safely
import os
import streamlit as st

if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)


# 3. Create the chat system memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle new user typing
if user_prompt := st.chat_input("Say something to Ariam..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Call Ariam's brain
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="Your name is Ariam. You are a helpful, friendly, and smart native AI assistant."
        )
        response = model.generate_content(user_prompt)
        
        # Show Ariam's answer
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Ariam is having trouble connecting right now. Please try again!")
