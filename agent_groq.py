from dotenv import load_dotenv

from livekit import agents
from livekit.agents import WorkerOptions, cli, function_tool, RunContext, Agent, AgentSession, RoomInputOptions
from livekit.plugins import (
    groq,
    cartesia,
    silero,
    noise_cancellation,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from datetime import datetime
import random

load_dotenv()

# Keep all the existing function tools and GroqAssistant class unchanged
@function_tool
async def get_current_time(context: RunContext) -> str:
    """Get the current time and date."""
    now = datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"

@function_tool
async def get_weather(context: RunContext, location: str) -> str:
    """Get weather information for a location."""
    weather_conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "snowy"]
    temperature = random.randint(60, 85)
    condition = random.choice(weather_conditions)
    return f"The weather in {location} is currently {condition} with a temperature of {temperature}°F"

class GroqAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant powered by Groq's fast LLM inference. 
            You can help with time, weather, and general questions. You're known for being very responsive 
            thanks to Groq's lightning-fast processing capabilities.""",
            tools=[get_current_time, get_weather]
        )

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    session = AgentSession(
        stt=groq.STT(model="whisper-large-v3"),
        llm=groq.LLM(model="llama3-70b-8192"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )
    await session.start(
        room=ctx.room,
        agent=GroqAssistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )
    await session.generate_reply(
        instructions="Greet the user warmly and mention that you're powered by Groq for super-fast responses!"
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))