import { Injectable } from '@nestjs/common';
import { ChatOpenAI } from '@langchain/openai';
import { BaseChatModel } from '@langchain/core/language_models/chat_models';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { SystemMessage, HumanMessage } from '@langchain/core/messages';
import { MessageContent } from '@langchain/core/messages';

interface TextContent {
  type: 'text';
  text: string;
}

interface ImageUrlContent {
  type: 'image_url';
  image_url: string;
}

type MessageContentItem = TextContent | ImageUrlContent;

@Injectable()
export class AgentFactory {
  private createBaseModel(temperature: number): BaseChatModel {
    return new ChatOpenAI({
      modelName: 'gpt-3.5-turbo',
      temperature,
      openAIApiKey: process.env.OPENAI_API_KEY,
    });
  }

  private convertMessageContentToString = (content: MessageContent): string => {
    if (typeof content === 'string') {
      return content;
    }
    if (Array.isArray(content)) {
      return content.map(item => {
        if (typeof item === 'string') return item;
        const typedItem = item as MessageContentItem;
        if (typedItem.type === 'text') {
          return typedItem.text;
        }
        if (typedItem.type === 'image_url') {
          return '[Image]';
        }
        return '';
      }).join(' ');
    }
    const typedContent = content as MessageContentItem;
    if (typedContent.type === 'text') {
      return typedContent.text;
    }
    if (typedContent.type === 'image_url') {
      return '[Image]';
    }
    return '';
  };

  createCharacterAgent(name: string, role: string, backstory: string) {
    const model = this.createBaseModel(0.7);
    const parser = new StringOutputParser();
    const convertContent = this.convertMessageContentToString;

    return {
      name,
      role,
      backstory,
      model,
      async generateResponse(context: string) {
        console.log(`Generating response for ${name} with context: ${context}`);
        const response = await model.invoke([
          new SystemMessage(`You are ${name}, a ${role}, with the following backstory: ${backstory}`),
          new HumanMessage(context)
        ]);
        const contentString = convertContent(response.content);
        return parser.invoke(contentString);
      }
    };
  }

  createManagerAgent() {
    const model = this.createBaseModel(0.5);
    const parser = new StringOutputParser();
    const convertContent = this.convertMessageContentToString;

    return {
      role: 'Conversation Manager',
      model,
      async createProfiles() {
        const response = await model.invoke([
          new SystemMessage('You are a conversation manager.'),
          new HumanMessage('Create two unique character profiles for a conversation. Include name, role, and backstory for each.')
        ]);
        const contentString = convertContent(response.content);
        return parser.invoke(contentString);
      },
      async monitorConversation(messages: any[]) {
        // Implement conversation monitoring logic
      }
    };
  }

  createAnalyticsAgent() {
    const model = this.createBaseModel(0.3);
    const parser = new StringOutputParser();
    const convertContent = this.convertMessageContentToString;

    return {
      role: 'Analytics Agent',
      model,
      async generateReport(messages: any[]) {
        const response = await model.invoke([
          new SystemMessage('You are an analytics agent that analyzes conversations.'),
          new HumanMessage(`Analyze the following conversation and generate a report: ${JSON.stringify(messages)}`)
        ]);
        const contentString = convertContent(response.content);
        return parser.invoke(contentString);
      }
    };
  }
} 