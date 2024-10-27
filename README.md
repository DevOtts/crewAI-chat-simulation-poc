# CrewAI Chat Simulation POC

This proof of concept demonstrates the capabilities of CrewAI by simulating a managed conversation between two AI agents with analytics tracking.

## Overview

This POC implements a chat simulation system with the following features:

1. **Automated Conversation**: Two AI agents engage in natural conversation based on their assigned personas
2. **Image Sharing Management**: A manager agent ensures that 10-15% of messages include images
3. **Analytics Tracking**: An analytics agent monitors conversation metrics and generates reports every 10 interactions

### Key Components

- **Character Agents**: AI-powered conversationalists with unique personas
- **Manager Agent**: Oversees conversation flow and image sharing ratios
- **Analytics Agent**: Tracks metrics and generates performance reports
- **Conversation Metrics**: Tracks message counts, image ratios, and engagement patterns

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crewai-chat-simulation.git
   cd crewai-chat-simulation
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

### Usage

1. Start the simulation:
   ```bash
   python main.py
   ```

2. The simulation will:
   - Create two AI characters with unique personas
   - Run conversations between them
   - Generate analytics reports every 10 interactions
   - Continue for 24 hours (configurable)

## Project Structure

- `main.py`: Entry point and simulation controller
- `agents.py`: Agent factory and configuration
- `tasks.py`: Task definitions and factory
- `models.py`: Data models for messages and metrics

## Monitoring

The simulation provides real-time feedback:
- Console output shows conversation progress
- Analytics reports display every 10 interactions
- Message and image ratios are continuously monitored

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
