from crewai import Task
from agents import AgentFactory
from datetime import datetime

class TaskFactory:
    @staticmethod
    def create_conversation_task(agent1, agent2, context) -> Task:
        return Task(
            description=f"""
                Engage in a natural conversation between {agent1.role} and {agent2.role}.
                Consider the following context: {context}
                Remember to occasionally share images (use [IMAGE] placeholder)
            """,
            agent=agent1.agent,  # Access the underlying Agent object
            expected_output="Conversation log with messages and image placeholders"
        )

    @staticmethod
    def create_management_task(manager_agent, conversation_log) -> Task:
        return Task(
            description=f"""
                1. Review the conversation log
                2. Calculate current image ratio
                3. Provide guidance if needed
                Current conversation: {conversation_log}
            """,
            agent=manager_agent.agent,
            expected_output="Management report and intervention if needed"
        )

    @staticmethod
    def create_analytics_task(analytics_agent, conversation_data) -> Task:
        return Task(
            description=f"""
                Generate analytics report for the following metrics:
                1. Messages sent/received per participant
                2. Image ratios
                3. Engagement patterns
                Data: {conversation_data}
            """,
            agent=analytics_agent.agent,
            expected_output="Detailed analytics report"
        )
