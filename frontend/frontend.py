import streamlit as st
import streamlit_authenticator as stauth

# PAGE NAME
st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

# --- Session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- Authentication ---
def login():
    st.title("Welcome to RAG Chat")
    st.write("This tool helps you interact with a custom knowledge base.")
    st.write("[GitHub Repository](https://github.com/your/repo)")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "demo" and password == "demo123":
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials")

if not st.session_state.authenticated:
    login()
    st.stop()

# # --- Sidebar ---
# st.sidebar.title("Admin Panel")
# admin_password = st.sidebar.text_input("Enter Admin Password", type="password")

# if admin_password == "adminpw":
#     st.session_state.is_admin = True
#     st.sidebar.success("Admin access granted")
# else:
#     st.session_state.is_admin = False
#     st.sidebar.warning("Admin access denied")

# st.sidebar.markdown("### LLM Settings")
# temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01, disabled=not st.session_state.is_admin)
# max_length = st.sidebar.slider('max_length', min_value=1, max_value=256, value=128, step=1, disabled=not st.session_state.is_admin)
# top_k = st.sidebar.slider('top_k', min_value=1, max_value=20, value=5, step=1, disabled=not st.session_state.is_admin)


# # --- Header ---
# st.title("Ask Your Custom AI")
# st.markdown("[GitHub Repository](https://github.com/your/repo)", unsafe_allow_html=True)

# # Store LLM generated responses
# if "messages" not in st.session_state.keys():
#     st.session_state.messages = [{"role": "assistant", "content": "Ask me something about Jan!"}]

# # Display or clear chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "Ask me something about Jan!"}]

# # User-provided prompt
# if prompt := st.chat_input(): #disabled = not replicate_api
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)

# # Generate a new response if last message is not from assistant
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             # response = generate_response(prompt)
#             response = ["Dummy response for demonstration purposes."]
#             placeholder = st.empty()
#             full_response = ''
#             for item in response:
#                 full_response += item
#                 placeholder.markdown(full_response)
#             placeholder.markdown(full_response)
#     message = {"role": "assistant", "content": full_response}
#     st.session_state.messages.append(message)

# st.button("Clear Chat History", on_click=clear_chat_history)


# # USER CREDENTIALS
# credentials = {
#     "usernames": {
#         "alice": {
#             "name": "jan",
#             "password": "123"
#         }
#     }
# }

# # Setup authenticator
# authenticator = stauth.Authenticate(
#     credentials=credentials,
#     cookie_name="rag_app_cookie",
#     key="rag_app_auth",
#     cookie_expiry_days=30
# )

# # Login UI
# # name, auth_status, username = authenticator.login()
# authenticator.login()