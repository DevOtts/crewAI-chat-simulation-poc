from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from crewai import Agent

@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime
    is_image: bool = False

@dataclass
class ConversationMetrics:
    messages_sent: int = 0
    messages_received: int = 0
    images_sent: int = 0
    images_received: int = 0

    @property
    def images_sent_ratio(self) -> float:
        return self.images_sent / self.messages_sent if self.messages_sent > 0 else 0

    @property
    def images_received_ratio(self) -> float:
        return self.images_received / self.messages_received if self.messages_received > 0 else 0

@dataclass
class Participant:
    name: str
    role: str
    backstory: str
    agent: Agent = None
    metrics: ConversationMetrics = field(default_factory=ConversationMetrics)
