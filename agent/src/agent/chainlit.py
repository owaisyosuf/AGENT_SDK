

import chainlit as cl

@cl.on_message
async def on_message(message:cl.Message):
  await cl.Message(
    content=f"hello {message.content}"
  ).send()