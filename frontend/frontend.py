import streamlit as st

st.set_page_config(page_title="Jan's Portfolio RAG App", page_icon="🔥", layout="wide")

with st.sidebar:
    st.title('Here will be the authentication and the admin panel including functions')
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=1, max_value=256, value=128, step=1)
    top_k = st.sidebar.slider('top_k', min_value=1, max_value=20, value=5, step=1)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)