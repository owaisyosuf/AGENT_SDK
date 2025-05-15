from agents import Agent , Runner , AsyncOpenAI , set_default_openai_api , set_default_openai_client , set_tracing_disabled
# from agents.extensions.models.litellm_model import LitellmModel
import os
from dotenv import load_dotenv
load_dotenv()
set_tracing_disabled(True)
set_default_openai_api("chat_completions")



MODEL="gemini-2.0-flash"

api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
  raise ValueError("api key is not set")

external_client=AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)

# Global level agent
agent1=Agent(
  name="assistant",
  instructions="you are a helpfull assistant",
  model=MODEL
)

# agent using litellm
# agent2=Agent(
#   name="assistant",
#   instructions="you are a helpfull assistant",
#   model=LitellmModel(api_key=api_key, model=MODEL)
# )
result=Runner.run_sync(
  agent1,
  "what is ai give me short answer"
)

print(result.final_output)


