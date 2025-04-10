
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from dotenv import load_dotenv, find_dotenv
import os
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl

load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("api key is not found")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="assistant",
    instructions="you are a helpful assistant",
    model=model
)

@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="hi i am your ai assistant with streaming output"
    ).send()

@cl.on_message
async def start(message: cl.Message):
    history = cl.user_session.get("history")
    
    msg = cl.Message(content="")
    await msg.send()

    # Add user message to history before streaming
    history.append({"role": "user", "content": message.content})
    
    result = Runner.run_streamed(
        agent,
        history,
        config
    )
    
    # Stream the response
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)
    
    # Add assistant's final response to history after streaming is complete
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)


 

