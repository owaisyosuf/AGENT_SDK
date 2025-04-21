from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig , AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
import requests
import json

api_key = os.getenv("OPEN_ROUTER")

if not api_key:
    raise ValueError("your api key is not valid")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-small-24b-instruct-2501:free"


response = requests.post(
  url=f"https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {api_key}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "Hi, i have 1000 pkr i want you to convert into usd"
      }
    ]
  })
)


data = response.json()
print (data['choices'][0]['message']['content'])