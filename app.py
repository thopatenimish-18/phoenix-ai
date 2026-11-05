import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Phoenix - Study & Code Assistant 🔥",
    page_icon="🔥",
    layout="centered",
)

st.title("🔥 Phoenix: Study & Code Assistant")
st.write(
    "Your elite AI tutor for mastering tough concepts and debugging code cleanly."
)

# Initialize Gemini Client (reads from Streamlit cloud secrets)
client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))

# Store chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User input box
if user_prompt := st.chat_input(
    "Ask a study question or paste code to debug..."
):
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  # Generate AI response
  with st.chat_message("assistant"):
    with st.spinner("Phoenix is igniting a solution..."):
      system_instruction = (
          "You are Phoenix, an elite AI tutor and senior software engineer. "
          "Help students break down complex concepts using vivid analogies, and "
          "help programmers write clean code, troubleshoot errors, and debug step-by-step."
      )

      response = client.models.generate_content(
          model="gemini-2.0-flash",
          contents=user_prompt,
          config={"system_instruction": system_instruction},
      )
      ai_response = response.text
      st.markdown(ai_response)

  st.session_state.messages.append(
      {"role": "assistant", "content": ai_response}
  )
