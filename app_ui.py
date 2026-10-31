import streamlit as st
import requests


st.set_page_config(
    page_title="NexusAI | Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 NexusAI Assistant")
st.caption("Enterprise RAG System powered by FastAPI, ChromaDB & LLM")


API_URL = "http://127.0.0.1:8000/chat"


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am NexusAI's Enterprise Assistant. How can I help you regarding our platform, pricing, or security today?"}
    ]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Ask a question about NexusAI..."):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

  
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Searching knowledge base..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": prompt},
                    timeout=90
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("reply", "No response received.")
                    sources_used = data.get("sources_used", False)
                    
                   
                    if sources_used:
                        bot_reply += "\n\n*(Verified by NexusAI Knowledge Base)*"
                    
                    message_placeholder.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    err_msg = f"⚠️ Server Error ({response.status_code}): Please verify backend status."
                    message_placeholder.markdown(err_msg)
            except requests.exceptions.ConnectionError:
                err_msg = "⚠️ Failed to connect to FastAPI backend. Ensure `uvicorn main:app` is running on port 8000."
                message_placeholder.markdown(err_msg)
            except Exception as e:
                message_placeholder.markdown(f"⚠️ Error: {str(e)}")
