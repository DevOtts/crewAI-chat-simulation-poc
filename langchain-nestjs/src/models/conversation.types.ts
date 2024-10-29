export interface Message {
  sender: string;
  content: string;
  timestamp: Date;
  isImage: boolean;
}

export interface ConversationMetrics {
  messagesSent: number;
  messagesReceived: number;
  imagesSent: number;
  imagesReceived: number;
}

export interface Participant {
  name: string;
  role: string;
  backstory: string;
  metrics: ConversationMetrics;
} 