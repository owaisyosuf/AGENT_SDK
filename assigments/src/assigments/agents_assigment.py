from agents import Agent, Runner ,AsyncOpenAI, set_default_openai_api, set_default_openai_client, set_tracing_disabled
from dotenv import load_dotenv
import os 
import asyncio
load_dotenv()
set_tracing_disabled(True)
set_default_openai_api('chat_completions')
api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("api key is not found")

MODEL="gemini-2.0-flash"

external_client=AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(external_client)

web_agent=Agent(
    name="web agent",
    instructions="You are a web development agent. Your sole responsibility is to answer questions strictly related to web development.",
    model=MODEL,
    handoff_description="web development spacialist"
)

app_agent=Agent(
    name="app agent",
    instructions="You are a application development agent. Your sole responsibility is to answer questions strictly related to application development.",
    model=MODEL,
    handoff_description="application development spacialist"
)

backend_agent=Agent(
    name="backend agent",
    instructions="You are a backend development agent. Your sole responsibility is to answer questions strictly related to backend development.",
    model=MODEL,
    handoff_description="backend development spacialist"
)

devops_agent=Agent(
    name="devops agent",
    instructions="You are a devops development agent. Your sole responsibility is to answer questions strictly related to devops development.",
    model=MODEL,
    handoff_description="devops development spacialist"
)

agentic_ai_agent=Agent(
    name="agentic ai agent",
    instructions="Understand the user's application development request. If needed, call backend or devops agent tools to fulfill the requirement accurately.",
    model=MODEL,
    handoff_description="application development spacialist",
    tools=[
       backend_agent.as_tool(
           tool_name="backend_agent",
           tool_description="specialist in backend development"),
        devops_agent.as_tool(
           tool_name="devops_agent",
           tool_description="specialist in devops development")
    ])
panacloud_agent=Agent(
    name="panacloud agent",
    instructions="You are a supervisor agent. Carefully read the user's prompt and delegate the task to the appropriate agent. If no suitable agent is available, politely respond with, 'I am not responsible for this task.",
    model=MODEL,
    handoffs=[web_agent, app_agent, agentic_ai_agent]
)

async def main():
    result=Runner.run_streamed(
        panacloud_agent,
        "what is web design"
    )
    async for event in result.stream_events:
        print(event)
    # async for event in result.stream_events():
    #     # if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
    #     print(event)
asyncio.run(main())