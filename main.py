from crewai import Crew, Task  # Added Task import here
from agents import AgentFactory
from tasks import TaskFactory
from models import Message, Participant, ConversationMetrics
from datetime import datetime, timedelta
import time

class ChatSimulation:
    def __init__(self):
        self.manager_agent = AgentFactory.create_manager_agent()
        self.analytics_agent = AgentFactory.create_analytics_agent()
        self.conversation_log = []
        self.participants = []

    def setup_participants(self):
        # Let the manager create character profiles
        profiles_task = Task(
            description="Create two unique character profiles for a conversation",
            agent=self.manager_agent,
            expected_output="Two character profiles with name, role, and backstory separated by newlines"
        )
        profiles = self.manager_agent.execute_task(profiles_task)
        
        # Create participants based on manager's profiles
        for profile in profiles.split("\n\n"):
            name, role, backstory = self._parse_profile(profile)
            # Create an agent for the participant
            agent = AgentFactory.create_character_agent(name, role, backstory)
            # Create the participant with the agent
            participant = Participant(
                name=name, 
                role=role, 
                backstory=backstory,
                agent=agent
            )
            self.participants.append(participant)
            
    def run_simulation(self, duration_hours=24):
        end_time = datetime.now() + timedelta(hours=duration_hours)
        interaction_count = 0

        while datetime.now() < end_time:
            # Run a conversation round
            conversation_task = TaskFactory.create_conversation_task(
                self.participants[0],
                self.participants[1],
                self.conversation_log[-10:] if self.conversation_log else []
            )
            
            # Execute conversation
            crew = Crew(
                agents=[self.manager_agent, self.analytics_agent],
                tasks=[conversation_task]
            )
            result = crew.kickoff()
            
            # Process conversation results
            self._process_conversation(result)
            interaction_count += 1

            # Generate analytics report every 10 interactions
            if interaction_count % 10 == 0:
                self._generate_analytics_report()

            time.sleep(10)
            print(f"Waiting 10 seconds before next interaction")    # Prevent API rate limiting

    def _parse_profile(self, profile_text):
        """Parse the profile text into name, role, and backstory."""
        try:
            print(f"Parsing profile: {profile_text}")
            lines = profile_text.strip().split('\n')
            name = lines[0].split(':')[1].strip()
            role = lines[1].split(':')[1].strip()
            backstory = '\n'.join(lines[2:]).strip()
            return name, role, backstory
        except Exception as e:
            # Fallback values in case parsing fails
            return f"Character_{len(self.participants)}", "Generic Role", "Generic backstory"

    def _process_conversation(self, conversation_result):
        print(f"Processing conversation: {conversation_result}")
        # Implementation to process and store conversation results
        pass

    def _generate_analytics_report(self):
        analytics_task = TaskFactory.create_analytics_task(
            self.analytics_agent,
            self.conversation_log
        )
        report = self.analytics_agent.execute_task(analytics_task)
        print(f"\nAnalytics Report:\n{report}")

if __name__ == "__main__":
    simulation = ChatSimulation()
    simulation.setup_participants()
    simulation.run_simulation()
