from agents import Agent , Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import chainlit as cl
load_dotenv()
set_tracing_disabled(True)

API_KEY= os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("api key is not found")

provider=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

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


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="I'm your assistant, here to help you with all your questions related to application development, web development, and agentic AI."
    ).send()

@cl.on_message
async def start(message: cl.Message):
    history = cl.user_session.get("history")
    
    msg = cl.Message(content="")
    await msg.send()

    # Add user message to history before streaming
    history.append({"role": "user", "content": message.content})
    result = Runner.run_streamed(
        panacloud_agent,
        history)
    

    # Stream the response
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)
    await cl.Message(content=f"Running agent {result.last_agent.name}").send()
    
    # Add assistant's final response to history after streaming is complete
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
