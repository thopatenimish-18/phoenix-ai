import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# Insert Google Search Console verification meta tag
components.html(
    '<meta name="google-site-verification" content="<meta name="google-site-verification" content="tiR12X2gg_0rtRIbTC_671DyJ48ayNxchHgvPgB7spw" />">'

st.set_page_config(
    page_title="Phoenix AI - Study & Code Assistant for Students",
    page_icon="🔥",
    layout="centered",
)

st.title("🔥 Phoenix: Independent AI Assistant")
st.write("Powered by an independent open-source AI model.")

# Initialize Groq client
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
  st.error("GROQ_API_KEY is missing from Streamlit Secrets! Please add it in your settings.")
  st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
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

      try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt},
            ],
        )
        ai_response = response.choices[0].message.content
      except Exception as e:
        ai_response = f"An error occurred: {e}"

      st.markdown(ai_response)

  st.session_state.messages.append(
      {"role": "assistant", "content": ai_response}
  )
