from crewai import Agent
from textwrap import dedent

class AgentFactory:
    @staticmethod
    def create_character_agent(name: str, role: str, backstory: str) -> Agent:
        return Agent(
            role=role,
            goal=f"Engage in natural conversation as {name} based on the given backstory",
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
