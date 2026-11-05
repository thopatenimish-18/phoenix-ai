import streamlit as st
from google import genai

st.set_page_config(
    page_title="Phoenix - Study & Code Assistant 🔥",
    page_icon="🔥",
    layout="centered",
)

st.title("🔥 Phoenix: Study & Code Assistant")
st.write("Your elite AI tutor for mastering tough concepts and debugging code cleanly.")

client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if user_prompt := st.chat_input("Ask a study question or paste code to debug..."):
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    with st.spinner("Phoenix is igniting a solution..."):
      # CHANGE THIS TEXT to customize your AI's custom behavior, rules, and personality!
      system_instruction = (
          "You are Phoenix, an autonomous custom AI assistant. "
          "You specialize in strict, highly technical breakdowns, coding logic, "
          "and structured study guides."
      )

      response = client.models.generate_content(
          model="gemini-3.8-flash",
          contents=user_prompt,
          config={"system_instruction": system_instruction},
      )
      ai_response = response.text
      st.markdown(ai_response)

  st.session_state.messages.append(
      {"role": "assistant", "content": ai_response}
  )
