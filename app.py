import streamlit as st
from router import routing
from faq import ingest_faq_data, chain
from sqlite import handle_sql_query
from config import FAQ_PATH

if 'faq_loaded' not in st.session_state:
    try:
        ingest_faq_data(FAQ_PATH)
        st.session_state.faq_loaded = True
    except Exception as e:
        st.error(f"Error loading FAQ data: {e}")

st.title("E-commerce Chatbot")

def ask(query):
    try:
        # Get route from query
        route = routing(query).name

        if route == "faq":
            return chain(query)
        
        elif route == "sql":
            with st.spinner("Searching products..."):
                return handle_sql_query(query)
        else:
            return "I'm not sure how to answer that. Try asking about products or policies!"
            
    except Exception as e:
        return f"Sorry, something went wrong. Please try again! Error: {str(e)}"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "ai", 
        "content": "Welcome! I can help you:\n- Find products (e.g., 'laptops under 50000')\n- Answer policy questions (e.g., 'What is your return policy?')"
    })

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
query = st.chat_input("Ask your question here...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Get response
    response = ask(query)

    # Add AI response
    st.session_state.messages.append({"role": "ai", "content": response})
    with st.chat_message("ai"):
        st.markdown(response)

# Add a clear chat button in sidebar
with st.sidebar:
    st.markdown("### Options")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()