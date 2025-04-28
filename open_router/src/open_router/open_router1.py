
from agents import Agent, OpenAIChatCompletionsModel, Runner , AsyncOpenAI,set_tracing_disabled
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio

api_key = os.getenv("OPEN_ROUTER_KEY")

if not api_key:
    raise ValueError("your api key is not valid")

set_tracing_disabled(True)

external_client=AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# model=OpenAIChatCompletionsModel(
#     model="google/gemini-2.5-pro-exp-03-25:free",
#     openai_client=external_client
# )

async def main():
    agent=Agent(
        name="assistant",
        model=OpenAIChatCompletionsModel(model="google/gemini-2.5-pro-exp-03-25:free" , openai_client=external_client )
        
    )
    result=await Runner.run(agent, "who is the founder of pakistan ", )
    print (result.final_output)

asyncio.run(main())