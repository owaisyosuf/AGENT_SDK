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

@cl.on_chat_start
async def chat_start():
  cl.user_session.set("history" , [])
  await cl.Message(
    "i am a helpfull assistant "
  ).send()

  @cl.on_message
  async def On_Message(message:cl.Message):
    history=cl.user_session.get("history" )
    history.append ({"role":"user", "content": message.content})
    result=await Runner.run(
      agent,
      input=history,
      run_config=config
    )
    history.append ({"role":"assistant", "content": result.final_output})
    cl.user_session.set("history" , history)
    await cl.Message(
      result.final_output
    ).send()

