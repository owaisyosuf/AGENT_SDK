from agents import Agent , Runner , set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
set_tracing_disabled(True)

api_key=os.getenv("GEMINI_API_KEY")
 
if not api_key:
    raise ValueError("api key is not found")

MODEL="gemini-2.0-flash"


external_client= AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent1=Agent(
    name="assistant",
    instructions="you are a helpfull assistant",
    model=OpenAIChatCompletionsModel(model=MODEL,openai_client=external_client )
)

result=Runner.run_sync(
    agent1,
    "who is the founder of pakistan"
)

print(result.final_output)