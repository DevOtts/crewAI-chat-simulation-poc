# LangChain Chat Simulation - NestJS Implementation

This project implements an AI chat simulation system using NestJS and LangChain, inspired by the CrewAI Python implementation.

## Features

- **Automated Conversation**: Two AI agents engage in natural conversation based on their assigned personas
- **Image Sharing Management**: Manages image sharing ratios in conversations
- **Analytics Tracking**: Monitors conversation metrics and generates periodic reports

## Prerequisites

- Node.js 16 or higher
- npm or yarn
- OpenAI API key

## Installation

1. Clone the repository and navigate to the project:
   ```bash
   cd langchain-nestjs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Project Structure

- `src/agents/`: Agent factory and configurations
- `src/models/`: TypeScript interfaces and types
- `src/modules/`: NestJS modules
- `src/services/`: Business logic and simulation services

## Running the Application

1. Build the project:
   ```bash
   npm run build
   ```

2. Start the simulation:
   ```bash
   npm run start
   ```

## Development

1. Start in development mode:
   ```bash
   npm run start:dev
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 