import streamlit as st
import requests
import os

st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

BACKEND_URL = os.environ.get("BACKEND_URL")

# --- Session state ---
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey there!"}]
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0
if "prompt_limit" not in st.session_state:
    st.session_state.prompt_limit = 0
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Helpers ---
def fetch_me():
    if st.session_state.token:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        me = requests.get(f"{BACKEND_URL}/me", headers=headers)
        if me.status_code == 200:
            info = me.json()
            st.session_state.prompt_count = info["prompt_count"]
            st.session_state.prompt_limit = info["prompt_limit"]
            st.session_state.is_admin = info.get("is_admin", False)
            st.session_state.username = info.get("username", "")
            return True
        else:
            # Token expired or invalid
            st.session_state.token = None
            st.session_state.page = "login"
            return False
    return False

def login(username, password):
    resp = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        st.session_state.token = token
        st.session_state.page = "chat"
        fetch_me()
        st.success("Login successful!")
        st.rerun()
    elif resp.status_code == 429:
        st.warning("You have reached the login limit. Please wait and try again later.")
    else:
        st.error("Login failed.")
        st.session_state.token = None

def logout():
    st.session_state.token = None
    st.session_state.page = "login"
    st.session_state.messages = [{"role": "assistant", "content": "Hey there!"}]
    st.session_state.prompt_count = 0
    st.session_state.prompt_limit = 0
    st.session_state.is_admin = False
    st.session_state.username = ""

# --- PAGE LOGIC ---
if st.session_state.page == "login":
    st.title("Welcome to Jan's Portfolio RAG App 🔥")
    st.caption("This app allows you to interact with a RAG model that can answer questions about Jan.")
    st.write("---")
    st.write("Upon successful login, you can chat with the AI model and ask questions about Jan's portfolio, skills, and experiences. Please log in to continue.")
    if not st.session_state.token:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.button("Login")
        if login_btn:
            login(username, password)
    else:
        fetch_me()
        st.session_state.page = "chat"
        st.rerun()

    # Footer/info
    for _ in range(11):
        st.write("")
    st.markdown("""
        ### About this App  
        [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
    """)

elif st.session_state.page == "chat":
    # --- Sidebar ---
    # st.sidebar.title("Admin Panel")
    if st.session_state.is_admin:
        st.sidebar.success("Admin access granted")
    else:
        st.sidebar.error("Admin access denied")
        st.sidebar.caption("Your role does not allow admin actions.")
    for _ in range(2):
        st.sidebar.write("")
    st.sidebar.markdown("### LLM Settings")
    temperature = float(st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01, disabled=not st.session_state.is_admin))
    max_tokens = int(st.sidebar.slider('max_tokens', min_value=1, max_value=512, value=256, step=1, disabled=not st.session_state.is_admin))
    top_k = int(st.sidebar.slider('top_k', min_value=1, max_value=20, value=10, step=1, disabled=not st.session_state.is_admin))
    model = str(st.sidebar.selectbox('Model', ['gpt-3.5-turbo', 'gpt-4', 'gpt-4.1'], disabled=not st.session_state.is_admin))

    for _ in range(4):
        st.sidebar.write("")
    st.sidebar.markdown("""
        [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
    """)
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    # --- Main content ---
    # --- Logic ---
    fetch_me()  # Always refresh state from backend
    def ask_backend(prompt, temperature, max_tokens, top_k, model):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        # Send request to backend
        data = {
            "query": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_k": top_k,
            "model": model
        }
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    r = requests.post(f"{BACKEND_URL}/rag", json=data, headers=headers)
            if r.status_code == 200:
                result = r.json()
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": result.get("answer", "No answer found.")})
                # Update prompt count
                st.session_state.prompt_count = result.get("prompt_count", st.session_state.prompt_count + 1)
                st.rerun()
            elif r.status_code == 403:
                st.error("Prompt limit reached.")
            elif r.status_code == 429:
                st.warning("You have reached the prompt limit (10 per Minute). Please wait and try again later.")
            elif r.status_code == 401:
                st.error("Session expired. Please log in again.")
                logout()
                st.rerun()
            else:
                st.error(f"API error: {r.text}")
        except Exception as ex:
            st.error(f"Request failed: {ex}")

    remaining = st.session_state.prompt_limit - st.session_state.prompt_count

    # --- Layout ---
    st.title("Ask me something about Jan 🔥")
    st.caption("Take the answers with a grain of salt, they are generated by an AI model and may not always be accurate. " \
    "Also, a RAG system is only as good as the data it has access to. As I did not provide every detail about my life, " \
    "the answers may be incomplete or not fully representative of my skills and experiences.")
    st.write("---")
    # Example prompts
    def on_click_example_prompt(prompt):
        if remaining > 0:
            ask_backend(prompt, temperature, max_tokens, top_k, model)
    example_prompt = None
    cols = st.columns(3)
    if cols[0].button("Why should we hire Jan?", disabled=(remaining == 0)):
        example_prompt = "Why should we hire Jan?"
    if cols[1].button("How could Jan contribute to our team?", disabled=(remaining == 0)):
        example_prompt = "How could Jan contribute to our team?"
    if cols[2].button("Give me a structured overview of Jan's career path", disabled=(remaining == 0)):
        example_prompt = "Give me a structured overview of Jan's career path"
    st.warning("Clicking these buttons **WILL** count towards your prompt limit.")
    st.write("---")
    if example_prompt:
        ask_backend(example_prompt, temperature, max_tokens, top_k, model)

    # Show chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Prompt input
    prompt = st.chat_input(disabled=(remaining == 0))
    if prompt and remaining > 0:
            ask_backend(prompt, temperature, max_tokens, top_k, model)

    # Display remaining prompts
    if remaining <= 0:
        st.error("You have reached your prompt limit. Contact Jan for more prompts.")
    st.markdown(f"**Prompts remaining:** {remaining}")

#     # # Clear that history button
#     # def clear_chat_history():
#     #     st.session_state.messages = [{"role": "assistant", "content": "Ask me something about Jan!"}]
#     # st.button("Clear Chat History", on_click=clear_chat_history)
