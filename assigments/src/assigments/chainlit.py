import chainlit as cl
import httpx

FAST_API_URL="http://localhost:8000/llm"


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        "i am a helpfull assistant").send()
    
@cl.on_message
async def on_message(message:cl.Message):
    history=cl.user_session.get("history")
    history.append({"role":"user", "content":message.content})
    