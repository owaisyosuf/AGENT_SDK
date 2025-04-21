
from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig , AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio

api_key = os.getenv("OPEN_ROUTER")

if not api_key:
    raise ValueError("your api key is not valid")

external_client=AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

model=OpenAIChatCompletionsModel(
    model="google/gemini-2.5-pro-exp-03-25:free",
    openai_client=external_client
)
congig=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

async def main():
    agent=Agent(
        name="assistant",
        model=model
    )
    result=await Runner.run(agent, "who is the founder of pakistan ", run_config=congig)
    print (result.final_output)

asyncio.run(main())