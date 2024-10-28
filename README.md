# CrewAI Chat Simulation POC

This proof of concept demonstrates the capabilities of CrewAI by simulating a managed conversation between two AI agents with analytics tracking, using a Streamlit web interface.

![Streamlit UI Screenshot](/blob/streamlit-ui.png)

## Overview

This POC implements a chat simulation system with the following features:

1. **AI-Generated Characters**: Automatically generates two unique characters with contrasting backgrounds and viewpoints
2. **Automated Conversation**: Two AI agents engage in natural conversation based on their generated personas
3. **Real-time Analytics**: Tracks conversation metrics and displays them in real-time
4. **Interactive UI**: Built with Streamlit for easy interaction and visualization

### Key Components

- **Character Generation**: AI-powered creation of unique personas
- **Conversation Agents**: Dynamic interaction between generated characters
- **Analytics Dashboard**: Real-time tracking of message counts and conversation duration
- **Interactive Controls**: Start/stop simulation and view conversation progress

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

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

### Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run main.py
   ```

2. The application will open in your default web browser

### Using the Application

1. **Generate Characters**:
   - Click the "Generate Characters" button
   - Review the generated character profiles
   - Characters are created with contrasting viewpoints for engaging dialogue

2. **Start Simulation**:
   - Click "Start Simulation" to begin the conversation
   - Watch as the characters engage in natural dialogue
   - The conversation runs for 5 turns by default

3. **Monitor Analytics**:
   - View real-time metrics in the right panel
   - Track message counts and conversation duration
   - Review the activity log for a history of interactions

## Project Structure

- `main.py`: Streamlit application and main logic
- `agents.py`: Agent factory and conversation management
- `models.py`: Data models for messages and metrics
- `requirements.txt`: Project dependencies

## Monitoring

The simulation provides real-time feedback through the Streamlit UI:
- Live conversation display
- Message count metrics
- Conversation duration tracking
- Activity log with timestamps

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

If you encounter issues:

1. Ensure your OpenAI API key is correctly set in `.env`
2. Check that all dependencies are installed
3. Verify Python version compatibility
4. Clear Streamlit cache if experiencing UI issues:
   ```bash
   streamlit cache clear
   ```

## Notes

- The simulation is limited to 5 turns by default (configurable in `main.py`)
- Characters are randomly generated but ensure contrasting viewpoints
- Responses have a 3-second delay to simulate natural conversation flow
