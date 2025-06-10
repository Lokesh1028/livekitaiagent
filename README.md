# LiveKit Voice Agent

A voice AI agent built with LiveKit's Agent Framework 1.x that supports real-time speech-to-text, language model processing, and text-to-speech capabilities.

## Features

- **Real-time voice conversation** with STT-LLM-TTS pipeline
- **Function tools** for extended capabilities (time, weather, calculations, reminders)
- **Noise cancellation** powered by LiveKit Cloud
- **Turn detection** for natural conversation flow
- **Multiple AI providers** integration (Deepgram, OpenAI, Cartesia)
- **Console and web modes** for testing and deployment

## Prerequisites

- Python 3.9 or later
- LiveKit Cloud account (or self-hosted LiveKit server)
- API keys for your chosen AI providers (see comparison below)

### AI Provider Options

| **LLM Providers** | **Strengths** | **Best For** |
|-------------------|---------------|--------------|
| **OpenAI** | High quality, widely supported | General purpose, complex reasoning |
| **Groq** | Ultra-fast inference (10x faster) | Real-time applications, cost optimization |
| **Anthropic Claude** | Safety-focused, excellent reasoning | Analysis, creative writing, ethical AI |
| **Google Gemini** | Multimodal, multilingual | Creative tasks, translations, vision |
| **AWS Bedrock** | Enterprise-grade, multiple models | Large organizations, compliance |
| **Ollama** | Local, private, free | Privacy-focused, offline applications |

| **STT Providers** | **Strengths** | **Best For** |
|-------------------|---------------|--------------|
| **Deepgram** | Fast, accurate, cost-effective | Recommended for most use cases |
| **OpenAI Whisper** | High accuracy, multilingual | High-quality transcription |
| **Google Cloud** | Good accuracy, Google ecosystem | Google-integrated applications |

| **TTS Providers** | **Strengths** | **Best For** |
|-------------------|---------------|--------------|
| **Cartesia** | High quality, fast, affordable | Recommended for most use cases |
| **ElevenLabs** | Premium voice quality, cloning | High-end applications, custom voices |
| **OpenAI TTS** | Good quality, simple | OpenAI-integrated applications |

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a .env file 
```

Edit the `.env` file with your actual API keys:

```env
# LiveKit Cloud Configuration (Required)
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here
LIVEKIT_URL=wss://your-project.livekit.cloud

# AI Provider API Keys for Groq Agent
GROQ_API_KEY=your_groq_api_key_here
CARTESIA_API_KEY=your_cartesia_api_key_here
```

### 3. Download Required Models

```bash
python agent_groq.py download-files
```

## Usage

Test your agent in different modes:

### Console Mode (Local Testing)
```bash
python agent_groq.py console
```
Speak directly with the agent using your computer's microphone and speakers.

### Development Mode
```bash
python agent_groq.py dev
```
Connect to LiveKit and use the [Agents Playground](https://agents.livekit.io/) for web interaction.

### Production Mode
```bash
python agent_groq.py start
```
Run the agent with production optimizations.

## Running the Agent

### Groq-Powered Voice Agent (`agent_groq.py`)

A lightning-fast voice assistant powered entirely by Groq:

- **STT**: Groq Whisper Large V3 (ultra-fast speech recognition)
- **LLM**: Groq Llama 3 70B (powerful conversation model)
- **TTS**: Cartesia Sonic (high-quality voice synthesis)
- **Function Tools**: Time, weather, and general assistance

#### **Features:**
- ⚡ **Ultra-fast responses** - Groq's optimized inference
- 🎙️ **Real-time voice conversation** 
- 🛠️ **Function calling** - Get time, weather, calculations
- 🔊 **High-quality voice** - Cartesia TTS
- 🎯 **Accurate transcription** - Groq Whisper

#### **Run Commands:**

**Console Mode (Local Testing):**
```bash
python agent_groq.py console
```

**Development Mode (Connect to LiveKit):**
```bash
python agent_groq.py dev
```

**Production Mode:**
```bash
python agent_groq.py start
```

## Architecture

```
User Audio → Groq Whisper STT → Groq Llama 3 LLM → Cartesia TTS → User Audio
                                      ↓
                              Function Tools
                              - Time/Date
                              - Weather
                              - General Assistance
```

## Customization

### Changing AI Providers

LiveKit Agent Framework supports **15+ AI providers**. You can mix and match:

#### **LLM Providers (Language Models)**
```python
# OpenAI (Original)
llm=openai.LLM(model="gpt-4o-mini")

# Groq (Lightning fast)
llm=groq.LLM(model="llama3-8b-8192")

# Anthropic Claude
llm=anthropic.LLM(model="claude-3-haiku-20240307")

# Google Gemini
llm=google.LLM(model="gemini-1.5-flash")

# AWS Bedrock (Multiple models)
llm=aws.LLM(model="anthropic.claude-3-sonnet-20240229-v1:0")

# Ollama (Local models)
llm=openai.LLM(model="llama3", base_url="http://localhost:11434/v1/")
```

#### **STT Providers (Speech-to-Text)**
```python
# Deepgram (Recommended)
stt=deepgram.STT(model="nova-3")

# OpenAI Whisper
stt=openai.STT(model="whisper-1")

# Google Cloud Speech
stt=google.STT()

# Azure Speech
stt=azure.STT()
```

#### **TTS Providers (Text-to-Speech)**
```python
# Cartesia (High quality)
tts=cartesia.TTS(model="sonic-2")

# ElevenLabs (Premium voices)
tts=elevenlabs.TTS(voice="Josh")

# OpenAI TTS
tts=openai.TTS(voice="nova")

# Google Cloud TTS
tts=google.TTS()
```

### Complete Mix-and-Match Example
```python
session = AgentSession(
    stt=deepgram.STT(model="nova-3"),      # Fast, accurate
    llm=groq.LLM(model="llama3-8b-8192"), # Lightning fast inference
    tts=elevenlabs.TTS(voice="Josh"),      # Premium voice quality
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),
)
```

### Adding Custom Tools

Create new function tools:

```python
@function_tool
async def my_custom_tool(context: RunContext, parameter: str) -> str:
    """Description of what this tool does."""
    # Your logic here
    return "Result"

# Add to agent
class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="Your instructions",
            tools=[my_custom_tool]  # Add your tool here
        )
```

### Modifying Agent Personality

Update the agent's instructions:

```python
class CustomAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a friendly assistant specialized in..."
        )
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure all required environment variables are set
2. **Model Download Fails**: Run `python agent.py download-files` again
3. **Audio Issues**: Check microphone permissions and audio device settings
4. **Connection Issues**: Verify LiveKit credentials and network connectivity

### Debug Mode

Add logging to debug issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Features

### Multi-Agent Handoff

Create workflows with multiple specialized agents. See LiveKit documentation for examples.

### Telephony Integration

Connect your agent to phone systems using LiveKit's SIP integration.

### Custom Frontend

Build web or mobile apps using LiveKit's client SDKs to create custom user interfaces.

## Documentation

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Agent Framework GitHub](https://github.com/livekit/agents)
- [LiveKit Cloud](https://livekit.io/cloud)

## License

This project is open source and available under the Apache 2.0 License. 