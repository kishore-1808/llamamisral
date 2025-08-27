import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

# -------------------------
# Streamlit Page Setup
# -------------------------
st.set_page_config(page_title="Kishore's Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Kishore's Assistant")

# -------------------------
# Chat UI
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # -------------------------
    # LangChain Prompt + Model
    # -------------------------
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Your name is Kishore's Assistant."),
        ("user", "user query: {query}")
    ])

    llm = Ollama(
        model="mistral",   # ⚡ Faster than llama2
        base_url="https://minichatgpt.streamlit.app/"
    )

    chain = template | llm | StrOutputParser()

    # -------------------------
    # Stream response (no streaming=True here)
    # -------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in chain.stream({"query": prompt}):   # <--- stream here
            full_response += chunk
            placeholder.markdown(full_response + "▌")  # cursor effect
        placeholder.markdown(full_response)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
