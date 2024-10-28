from crewai import Crew
from agents import AgentFactory
from models import Message, Participant, ConversationMetrics, ChatHistory
from datetime import datetime
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
if 'conversation_turn' not in st.session_state:
    st.session_state.conversation_turn = 0

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
        # Create agents for both participants
        agent1 = AgentFactory.create_conversation_agent(char1_name, char1_role, char1_backstory)
        agent2 = AgentFactory.create_conversation_agent(char2_name, char2_role, char2_backstory)
        
        st.session_state.chat_history.start_conversation()
        st.session_state.participants = [
            Participant(char1_name, char1_role, char1_backstory, agent1),
            Participant(char2_name, char2_role, char2_backstory, agent2)
        ]
        st.session_state.is_simulating = True
        st.session_state.conversation_turn = 0
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
        
        # Maximum turns for the conversation
        MAX_TURNS = 5
        
        if st.session_state.conversation_turn < MAX_TURNS:
            char1, char2 = st.session_state.participants
            current_sender = char1 if st.session_state.conversation_turn % 2 == 0 else char2
            
            # Get conversation history
            conversation_history = [
                f"{msg.sender}: {msg.content}"
                for msg in st.session_state.chat_history.get_all_messages()
            ]
            
            # Generate response using the agent
            if st.session_state.conversation_turn == 0:
                # First message is an introduction
                message = AgentFactory.create_response(
                    current_sender,
                    [],
                    "Start the conversation with an introduction"
                )
            else:
                # Generate response based on conversation history
                last_message = st.session_state.chat_history.messages[-1].content
                message = AgentFactory.create_response(
                    current_sender,
                    conversation_history,
                    last_message
                )
            
            st.session_state.chat_history.add_message(current_sender.name, message)
            st.session_state.conversation_turn += 1
            
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
    st.metric("Conversation Turns", st.session_state.conversation_turn)
    
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
