import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Phoenix - Independent AI 🔥",
    page_icon="🔥",
    layout="centered",
)

st.title("🔥 Phoenix: Independent AI Assistant")
st.write("Powered by an independent open-source AI model.")

# Initialize Groq client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets.get("GROQ_API_KEY"),
)

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if user_prompt := st.chat_input("Ask Phoenix anything..."):
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    with st.spinner("Phoenix is thinking..."):
      system_instruction = (
          "You are Phoenix, an independent custom AI assistant."
      )

      response = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
              {"role": "system", "content": system_instruction},
              {"role": "user", "content": user_prompt},
          ],
      )
      ai_response = response.choices[0].message.content
      st.markdown(ai_response)

  st.session_state.messages.append(
      {"role": "assistant", "content": ai_response}
  )
