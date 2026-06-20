import streamlit as st
import google.generativeai as genai

# 1. Page titles and headings
st.title("🤖 Chat with Ariam")
st.write("Welcome to Ariam's official home! Type a message below to talk to her.")

# 2. Put your exact original key directly here
API_KEY = "AQ.Ab8RN6IS-iZsNPr-O_hZjzWPEvbWcPv_vHiCnYcsokItflUVEg"
genai.configure(api_key=API_KEY)

# 3. Create the text history structure
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past texts on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Read what you type in the bar
if user_prompt := st.chat_input("Say something to Ariam..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Call Ariam's actual mind database
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Your name is Ariam. You are a helpful, friendly, and smart native AI assistant."
        )
        response = model.generate_content(user_prompt)
        
        # Display Ariam's response text
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Ariam is having trouble connecting right now. Please try again!")
