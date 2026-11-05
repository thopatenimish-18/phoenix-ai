import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# 1. Google Search Console Verification Tag
components.html(
    '<meta name="google-site-verification" content="tiR12X2gg_0rtRIbTC_671DyJ48ayNxchHgvPgB7spw">',
    height=0,
)

# 2. Page Configuration
st.set_page_config(
    page_title="Phoenix AI - Study & Code Assistant for Students",
    page_icon="🔥",
    layout="centered",
)

# 3. Initialize Student Login State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# 4. Student Login Screen
if not st.session_state.logged_in:
    st.title("🔥 Phoenix: Student Login")
    st.write("Enter your name or student ID to access your AI assistant.")

    with st.form("login_form"):
        name_input = st.text_input("Your Name / Student ID")
        submit_button = st.form_submit_button("Log In to Phoenix")

        if submit_button:
            if name_input.strip():
                st.session_state.logged_in = True
                st.session_state.student_name = name_input.strip()
                st.rerun()
            else:
                st.error("Please enter a valid name or ID to continue.")
    st.stop()

# 5. Sidebar & Logout
st.sidebar.write(f"👤 Logged in as: **{st.session_state.student_name}**")
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.student_name = ""
    st.session_state.messages = []
    st.rerun()

# 6. Main Chat Interface
st.title("🔥 Phoenix: Independent AI Assistant")
st.write(f"Hello, {st.session_state.student_name}! Powered by an independent open-source AI model.")

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
            system_instruction = "You are Phoenix, an independent custom AI assistant helping students."

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                ai_response = response.choices[0].message.content
            except Exception as e:
                ai_response = f"An error occurred: {e}"

            st.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
