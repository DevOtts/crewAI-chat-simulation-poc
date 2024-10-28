from crewai import Crew, Task
from agents import AgentFactory
from models import Message, Participant, ConversationMetrics, ChatHistory
from datetime import datetime
import time
import streamlit as st
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_profile(profile: str) -> tuple:
    """Parse a profile string into name, role, and backstory"""
    try:
        name_match = re.search(r'Name:\s*(.*?)(?=\s*Role:)', profile, re.DOTALL)
        role_match = re.search(r'Role:\s*(.*?)(?=\s*Backstory:)', profile, re.DOTALL)
        backstory_match = re.search(r'Backstory:\s*(.*?)(?=\s*(?:Name:|$))', profile, re.DOTALL)
        
        name = name_match.group(1).strip() if name_match else ""
        role = role_match.group(1).strip() if role_match else ""
        backstory = backstory_match.group(1).strip() if backstory_match else ""
        
        return name, role, backstory
    except Exception as e:
        logger.error(f"Error parsing profile: {e}")
        return "", "", ""

def extract_profiles(text: str) -> tuple:
    """Extract two profiles from the generated text"""
    # Split on double newline or when finding a new "Name:" section
    profiles = re.split(r'\n\n(?=Name:)|(?=Name:)', text)
    # Filter out empty strings and clean up
    profiles = [p.strip() for p in profiles if p.strip()]
    
    if len(profiles) >= 2:
        return profiles[0], profiles[1]
    else:
        logger.error(f"Could not find two profiles in text: {text}")
        return "", ""

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
    st.header("Conversation Setup")
    
    # Create a button to generate characters
    if st.button("Generate Characters"):
        # Create manager agent
        manager_agent = AgentFactory.create_manager_agent()
        
        # Create task for generating character profiles
        profiles_task = Task(
            description="Create two unique and interesting character profiles for a conversation. Make them have contrasting viewpoints or backgrounds to create engaging dialogue.",
            expected_output="""Two character profiles in the following format:
            Name: [character name]
            Role: [character role]
            Backstory: [detailed backstory]

            Name: [character name]
            Role: [character role]
            Backstory: [detailed backstory]"""
        )
        
        # Generate profiles
        profiles = manager_agent.execute_task(profiles_task)
        
        # Parse and store profiles in session state
        profile1, profile2 = extract_profiles(profiles)
        
        if profile1 and profile2:
            st.session_state.profile1 = profile1
            st.session_state.profile2 = profile2
            st.rerun()
        else:
            st.error("Failed to generate valid character profiles. Please try again.")

    # Display generated profiles if they exist
    if 'profile1' in st.session_state:
        st.subheader("Generated Characters")
        with st.expander("Character 1", expanded=True):
            st.text(st.session_state.profile1)
        with st.expander("Character 2", expanded=True):
            st.text(st.session_state.profile2)
        
        # Start simulation button
        if st.button("Start Simulation"):
            # Parse profiles and create agents
            char1_name, char1_role, char1_backstory = parse_profile(st.session_state.profile1)
            char2_name, char2_role, char2_backstory = parse_profile(st.session_state.profile2)
            
            agent1 = AgentFactory.create_character_agent(char1_name, char1_role, char1_backstory)
            agent2 = AgentFactory.create_character_agent(char2_name, char2_role, char2_backstory)
            
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
