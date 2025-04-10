from agents import Agent, Runner , OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from dotenv import load_dotenv , find_dotenv
import os
import chainlit as cl

load_dotenv(find_dotenv())

api_key=os.getenv("GEMINI_API_KEY")
 
if not api_key:
  raise ValueError("api key is not found")

external_client= AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model=OpenAIChatCompletionsModel(
  model="gemini-2.0-flash",
  openai_client=external_client
)

config=RunConfig(
  model=model,
  model_provider=external_client,
  tracing_disabled=True
)


agent = Agent(
  name="assistant",
  instructions="you are a helpfull assistant",
  model=model
)

@cl.on_message
async def chat(message : cl.Message):
  result=await Runner.run(
    agent,
    input=message.content,
    run_config=config
  )
  await cl.Message(
    result.final_output
  ).send()
