import streamlit as st

# PAGE NAME
st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

# --- Session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "prompt_limit" not in st.session_state:
    st.session_state.prompt_limit = 10  # Set a limit for the number of prompts
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0  # Initialize the prompt count


# --- Home page ---
if st.session_state.page == "login":
    st.title("Welcome to Jan's Portfolio RAG App 🔥")
    st.caption("This app allows you to interact with a RAG model that can answer questions about Jan.")
    st.write("---")
    st.write("Upon successful login, you can chat with the AI model and ask questions about Jan's portfolio, skills, and experiences. Please log in to continue.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "demo" and password == "demo123":
            st.session_state.authenticated = True
            st.session_state.page = "chat"
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
                ### About this App
                [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
                """)

# --- Chat page ---
elif st.session_state.page == "chat":
    # --- Sidebar ---
    st.sidebar.title("Admin Panel")
    admin_password = st.sidebar.text_input("Enter Password", type="password")
    if admin_password == "adminpw":
        st.session_state.is_admin = True
        st.sidebar.success("Admin access granted")
    else:
        st.session_state.is_admin = False
        st.sidebar.warning("Admin access denied")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.markdown("### LLM Settings")
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01, disabled=not st.session_state.is_admin)
    max_length = st.sidebar.slider('max_length', min_value=1, max_value=256, value=128, step=1, disabled=not st.session_state.is_admin)
    top_k = st.sidebar.slider('top_k', min_value=1, max_value=20, value=5, step=1, disabled=not st.session_state.is_admin)
    model = st.sidebar.selectbox('Model', ['gpt-3.5-turbo', 'gpt-4', 'gpt-4.1'], disabled=not st.session_state.is_admin)
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.markdown("""
                        [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/jan94z/portfolio-rag-mvp)
                        """)

    # --- Main content ---
    st.title("Ask me something about Jan 🔥")
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Hey there!"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # On chat page, before prompt input
    
    # User-provided prompt
    remaining = st.session_state.prompt_limit - st.session_state.prompt_count
    if prompt := st.chat_input(disabled=(remaining == 0)):
        if remaining > 0:
            st.session_state.prompt_count += 1
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
                if remaining == 10:
                    st.rerun()
        elif remaining <= 0:
            st.warning("You have reached your prompt limit.")
    
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # response = generate_response(prompt)
                response = ["Dummy response for demonstration purposes."]
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

    
    st.markdown(f"**Prompts remaining:** {remaining}")
    # # Clear that history button
    # def clear_chat_history():
    #     st.session_state.messages = [{"role": "assistant", "content": "Ask me something about Jan!"}]
    # st.button("Clear Chat History", on_click=clear_chat_history)
