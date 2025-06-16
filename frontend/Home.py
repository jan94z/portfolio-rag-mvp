import streamlit as st
import requests

st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

BACKEND_URL = "http://rag-api:8000/api/v1"

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
    st.sidebar.title("Admin Panel")
    if st.session_state.is_admin:
        st.sidebar.success("Admin access granted")
    else:
        st.sidebar.error("Admin access denied")
    st.sidebar.write("")
    st.sidebar.markdown("### LLM Settings")
    temperature = float(st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01, disabled=not st.session_state.is_admin))
    max_tokens = int(st.sidebar.slider('max_tokens', min_value=1, max_value=256, value=128, step=1, disabled=not st.session_state.is_admin))
    top_k = int(st.sidebar.slider('top_k', min_value=1, max_value=20, value=5, step=1, disabled=not st.session_state.is_admin))
    model = str(st.sidebar.selectbox('Model', ['gpt-3.5-turbo', 'gpt-4', 'gpt-4.1'], disabled=not st.session_state.is_admin))
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
    st.write("---")
    # Example prompts
    def on_click_example_prompt(prompt):
        if remaining > 0:
            ask_backend(prompt, temperature, max_tokens, top_k, model)
    cols = st.columns(3)
    cols[0].button("Why would I hire Jan?", on_click=lambda: on_click_example_prompt("Why would I hire Jan?"), disabled=(remaining == 0))
    cols[1].button("Dummy button 2", on_click=lambda: on_click_example_prompt("Dummy button 2 clicked!"), disabled=(remaining == 0))
    cols[2].button("Dummy button 3", on_click=lambda: on_click_example_prompt("Dummy button 3 clicked!"), disabled=(remaining == 0))
    st.warning("Clicking these buttons **WILL** count towards your prompt limit.")
    st.write("---")

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




# import streamlit as st
# import os
# import requests
# from fastapi import Query

# # PAGE NAME
# st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

# # API 
# BACKEND_URL = "http://rag-api:8000/api/v1"

# # --- Session state ---
# # if "authenticated" not in st.session_state:
# #     st.session_state.authenticated = False
# # if "is_admin" not in st.session_state:
# #     st.session_state.is_admin = False
# # if "page" not in st.session_state:
# #     st.session_state.page = "login"
# # if "prompt_limit" not in st.session_state:
# #     st.session_state.prompt_limit = 10  # Set a limit for the number of prompts
# # if "prompt_count" not in st.session_state:
# #     st.session_state.prompt_count = 0  # Initialize the prompt count
# if "token" not in st.session_state:
#     st.session_state.token = None  # Initialize token for authentication
# if "prompt_count" not in st.session_state:
#     st.session_state.prompt_count = 0
# if "prompt_limit" not in st.session_state:
#     st.session_state.prompt_limit = 0
# if "page" not in st.session_state:
#     st.session_state.page = "login"  # Default page is login

# # --- LOGIN LOGIC ---
# def login(username, password):
#     resp = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})
#     if resp.status_code == 200:
#         token = resp.json()["access_token"]
#         st.session_state.token = token
#         headers = {"Authorization": f"Bearer {token}"}
#         me = requests.get(f"{BACKEND_URL}/me", headers=headers).json()
#         st.session_state.prompt_count = me["prompt_count"]
#         st.session_state.prompt_limit = me["prompt_limit"]
#         st.session_state.username = me["username"]
#         return True
#     else:
#         st.error("Login failed.")
#         return False

# # --- Home page ---
# if st.session_state.page == "login":
#     st.title("Welcome to Jan's Portfolio RAG App 🔥")
#     st.caption("This app allows you to interact with a RAG model that can answer questions about Jan.")
#     st.write("---")
#     st.write("Upon successful login, you can chat with the AI model and ask questions about Jan's portfolio, skills, and experiences. Please log in to continue.")
#     if not st.session_state.token:
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if login(username, password):
#                 st.session_state.page = "chat"
#                 st.success("Login successful!")
#                 st.rerun()
#     else:
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         me = requests.get(f"{BACKEND_URL}/me", headers=headers)
#         if me.status_code == 200:
#             st.session_state.page = "chat"
#             me = me.json()
#             st.session_state.prompt_count = me["prompt_count"]
#             st.session_state.prompt_limit = me["prompt_limit"]
#             st.session_state.username = me["username"]
#         remaining = st.session_state.prompt_limit - st.session_state.prompt_count
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.write("")
#     st.markdown("""
#                 ### About this App
#                 [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
#                 """)

# # --- Chat page ---
# elif st.session_state.page == "chat":
#     # --- Sidebar ---
#     st.sidebar.title("Admin Panel")
#     if me["is_admin"]:
#         st.session_state.is_admin = True
#         st.sidebar.success("Admin access granted")
#     else:
#         st.session_state.is_admin = False
#         st.sidebar.error("Admin access denied")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.markdown("### LLM Settings")
#     temperature = float(st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01, disabled=not st.session_state.is_admin))
#     max_tokens = int(st.sidebar.slider('max_tokens', min_value=1, max_value=256, value=128, step=1, disabled=not st.session_state.is_admin))
#     top_k = int(st.sidebar.slider('top_k', min_value=1, max_value=20, value=5, step=1, disabled=not st.session_state.is_admin))
#     model = str(st.sidebar.selectbox('Model', ['gpt-3.5-turbo', 'gpt-4', 'gpt-4.1'], disabled=not st.session_state.is_admin))
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.markdown("""
#                         [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
#                         """)

#     # --- Main content ---
#     remaining = st.session_state.prompt_limit - st.session_state.prompt_count
#     st.title("Ask me something about Jan 🔥")
#     st.write("---")
#     # example prompts
#     def on_click_example_prompt(prompt):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.session_state.prompt_count += 1
#     cols = st.columns(3)

#     cols[0].button("Why would I hire Jan?", on_click=lambda: on_click_example_prompt("Why would I hire Jan?"), disabled=(remaining == 0))

#     cols[1].button("Dummy button 2", on_click=lambda: on_click_example_prompt("Dummy button 2 clicked!"), disabled=(remaining == 0))

#     cols[2].button("Dummy button 3", on_click=lambda: on_click_example_prompt("Dummy button 3 clicked!"), disabled=(remaining == 0))
#     st.warning("Clicking these buttons **WILL** count towards your prompt limit.")
#     st.write("---")
#     # Store LLM generated responses
#     if "messages" not in st.session_state.keys():
#         st.session_state.messages = [{"role": "assistant", "content": "Hey there!"}]

#     # Display or clear chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])
    
#     # User-provided prompt
#     if prompt := st.chat_input(disabled=(remaining == 0)):
#         if remaining > 0:

#             st.session_state.prompt_count += 1
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.write(prompt)
#                 st.rerun()
    
#     # Generate a new response if last message is not from assistant
#     if st.session_state.messages[-1]["role"] != "assistant":
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 full_response = requests.post(f"{BACKEND_URL}/rag", json={"query": str(st.session_state.messages[-1]), "top_k": int(top_k), "model": str(model), "max_tokens": int(max_tokens), "temperature": float(temperature)})
#                 answer = full_response.json().get("answer") 
#         message = {"role": "assistant", "content": answer}
#         st.session_state.messages.append(message)
#         st.rerun()

#     if remaining <= 0:
#         st.error("You have reached your prompt limit. Contact Jan for more prompts.")
#     st.markdown(f"**Prompts remaining:** {remaining}")
#     # # Clear that history button
#     # def clear_chat_history():
#     #     st.session_state.messages = [{"role": "assistant", "content": "Ask me something about Jan!"}]
#     # st.button("Clear Chat History", on_click=clear_chat_history)
