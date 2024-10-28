from crewai import Agent, Task
from textwrap import dedent
from typing import List
import os

class AgentFactory:
    @staticmethod
    def create_character_agent(name: str, role: str, backstory: str) -> Agent:
        return Agent(
            role=role,
            goal=f"Engage in a natural and short conversation as {name} based on the given backstory",
            backstory=dedent(backstory),
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            }
        )

    @staticmethod
    def create_manager_agent() -> Agent:
        return Agent(
            role="Conversation Manager",
            goal="Manage conversation flow and ensure image ratio stays between 10-15%",
            backstory=dedent("""
                You are responsible for:
                1. Creating character profiles for the two chatters
                2. Monitoring their conversation
                3. Ensuring image sharing ratio stays within bounds
                4. Intervening when necessary to maintain engagement
            """),
            verbose=True,
            allow_delegation=True,
            tools=[],
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.5
            }
        )

    @staticmethod
    def create_analytics_agent() -> Agent:
        return Agent(
            role="Analytics Agent",
            goal="Track and analyze conversation metrics",
            backstory=dedent("""
                You analyze conversation data and generate reports including:
                1. Message counts (sent/received)
                2. Image ratios
                3. Engagement metrics
                Generate reports every 10 interactions
            """),
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.3
            }
        )

    @staticmethod
    def create_conversation_agent(name: str, role: str, backstory: str) -> Agent:
        return Agent(
            role=f"{name} - {role}",
            goal=f"Engage in a natural and short conversation as {name}, a {role}, with the following backstory: {backstory}",
            backstory=backstory,
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "request_timeout": 120
            }
        )

    @staticmethod
    def create_response(participant, conversation_history: List[str], last_message: str) -> str:
        context = "\n".join(conversation_history)
        
        # Extract name and role from participant
        name = participant.name
        role = participant.role
        
        prompt = f"""
        You are {name}, a {role}.
        Backstory: {participant.backstory}
        
        Previous conversation:
        {context}
        
        Last message received: {last_message}
        
        Respond naturally as your character would, keeping in mind your role and backstory.
        Keep the response concise but engaging, and stay in character.
        """
        
        # Create a Task object with required fields
        task = Task(
            prompt=prompt,
            description="Generate a conversational response",
            expected_output="A natural and engaging response"
        )
        
        return participant.agent.execute_task(task)
