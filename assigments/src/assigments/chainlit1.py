import chainlit as cl
import httpx

FASTAPI_URL="http://localhost:8000/llm"


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        "i am a helpfull assistant").send()
    
@cl.on_message
async def on_message(message:cl.Message):
    history=cl.user_session.get("history")
    history.append({"role":"user", "content":message.content})
    async with httpx.AsyncClient() as client:
        response = await client.post(FASTAPI_URL, json={"prompt": message.content})
        if response.status_code == 200:
            agent_response = response.json().get("response")
        else:
            agent_response = "Error: Could not connect to the FastAPI endpoint."
    history.append({"role":"assistant", "content":agent_response})
    await cl.Message(content=agent_response).send()

