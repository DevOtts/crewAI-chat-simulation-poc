from crewai import Crew, Agent
from agents import AgentFactory
from tasks import TaskFactory
from models import Message, Participant, ConversationMetrics, ChatHistory
from datetime import datetime, timedelta
import time
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatHistory()
if 'is_simulating' not in st.session_state:
    st.session_state.is_simulating = False
if 'participants' not in st.session_state:
    st.session_state.participants = []

st.title("AI Chat Simulation POC")

# Create two columns: chat (2/3) and analytics (1/3)
chat_col, analytics_col = st.columns([2, 1])

with chat_col:
    st.header("Character Setup")
    
    # Character 1 setup
    st.subheader("Character 1")
    char1_name = st.text_input("Name", "Alice", key="char1_name")
    char1_role = st.text_input("Role", "Tech Enthusiast", key="char1_role")
    char1_backstory = st.text_area("Backstory", 
        "A passionate tech enthusiast who loves discussing AI and future technologies.", 
        key="char1_backstory")
    
    # Character 2 setup
    st.subheader("Character 2")
    char2_name = st.text_input("Name", "Bob", key="char2_name")
    char2_role = st.text_input("Role", "Philosophy Student", key="char2_role")
    char2_backstory = st.text_area("Backstory", 
        "A philosophy student interested in the ethical implications of AI.", 
        key="char2_backstory")
    
    # Start simulation button
    if st.button("Start Simulation"):
        st.session_state.chat_history.start_conversation()
        st.session_state.participants = [
            Participant(char1_name, char1_role, char1_backstory),
            Participant(char2_name, char2_role, char2_backstory)
        ]
        st.session_state.is_simulating = True
        logger.info("Starting new simulation...")
    
    # Display chat history
    st.subheader("Conversation")
    for msg in st.session_state.chat_history.get_all_messages():
        with st.chat_message(msg.sender):
            st.write(f"{msg.content}")
            st.caption(f"Sent at: {msg.timestamp.strftime('%H:%M:%S')}")

    # Simulate conversation if started
    if st.session_state.is_simulating:
        # Simulate a conversation exchange
        time.sleep(3)  # Add delay between messages
        
        # For now, just simulate basic exchanges
        # This will be replaced with actual CrewAI agent interactions
        if len(st.session_state.chat_history.messages) < 6:  # Limit to 3 exchanges
            char1, char2 = st.session_state.participants
            
            if len(st.session_state.chat_history.messages) % 2 == 0:
                message = f"Hi, I'm {char1.name} and I'm interested in {char1.role}."
                st.session_state.chat_history.add_message(char1.name, message)
            else:
                message = f"Nice to meet you! I'm {char2.name}, {char2.role}."
                st.session_state.chat_history.add_message(char2.name, message)
            
            st.rerun()
        else:
            st.session_state.is_simulating = False
            logger.info("Simulation completed")

with analytics_col:
    st.header("Analytics & Logs")
    
    metrics = st.session_state.chat_history.metrics
    
    # Display metrics
    st.metric("Total Messages", metrics.messages_count)
    st.metric("Conversation Duration (s)", round(metrics.conversation_duration, 1))
    
    # Create a section for logs
    st.subheader("Activity Log")
    log_placeholder = st.empty()
    
    # Display recent activities
    with log_placeholder:
        recent_messages = st.session_state.chat_history.messages[-5:]
        log_text = "\n".join([
            f"{msg.timestamp.strftime('%H:%M:%S')} - {msg.sender}: {msg.content}"
            for msg in recent_messages
        ])
        st.code(log_text)
