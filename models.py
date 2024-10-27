from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from crewai import Agent

@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime
    is_image: bool = False

@dataclass
class ConversationMetrics:
    messages_count: int = 0
    average_response_time: float = 0.0
    conversation_duration: float = 0.0
    
@dataclass
class Participant:
    name: str
    role: str
    backstory: str
    agent: Agent = None
    metrics: ConversationMetrics = field(default_factory=ConversationMetrics)

class ChatHistory:
    def __init__(self):
        self.messages: List[Message] = []
        self.start_time: datetime = None
        self.metrics: ConversationMetrics = ConversationMetrics()
    
    def start_conversation(self):
        self.start_time = datetime.now()
        self.messages.clear()
        self.metrics = ConversationMetrics()
    
    def add_message(self, sender: str, content: str):
        message = Message(
            sender=sender,
            content=content,
            timestamp=datetime.now()
        )
        self.messages.append(message)
        self.metrics.messages_count += 1
        
        if self.start_time:
            self.metrics.conversation_duration = (datetime.now() - self.start_time).total_seconds()
    
    def get_all_messages(self) -> List[Message]:
        return self.messages
