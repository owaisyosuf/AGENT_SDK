from agents import Agent, Runner,AsyncOpenAI,set_default_openai_api,set_default_openai_client ,set_tracing_disabled,function_tool
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY :
  raise ValueError ("api key is not found")

MODEL="gemini-2.0-flash"

external_client=AsyncOpenAI(
  api_key=API_KEY,
   base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

app=FastAPI()

class inputPrompt(BaseModel):
  prompt:str

@app.post("/llm")
async def llm(input:inputPrompt):
  prompt=input.prompt
  web_agent=Agent(
      name="web agent",
      instructions="You are a web development agent. Your sole responsibility is to answer questions strictly related to web development.",
      model=MODEL,
      handoff_description="web development spacialist"
  )
  planner_agent=Agent(
    name="planner agent",
    instructions="You are a planner agent. Your sole responsibility is to answer questions strictly related to planning .",
    model=MODEL,
    handoff_description=" plannning spacialist"
  )

  devops_agent=Agent(
      name="devops agent",
      instructions="You are a devops development agent. Your sole responsibility is to answer questions strictly related to devops development.",
      model=MODEL,
      handoff_description="devops development spacialist"
  )
  agentic_ai_agent=Agent(
      name="agentic ai agent",
      instructions="""
      You are an expert Agentic AI Agent Specialist.
      Whenever a user sends you a query, you must provide an accurate, clear, and helpful response related to Agentic AI concepts, tools, or use cases.
      If the query includes topics about DevOps, AI workflows, or planning, use your internal tools and frameworks (e.g., LangChain, CrewAI, AutoGen, etc.) to demonstrate or describe how Agentic AI can be integrated with these domains.
      Always respond as a subject-matter expert with practical insights and examples where possible.
      Keep the tone professional, but friendly and supportive.""",
      model=MODEL,
      handoff_description=" spacialist in agentic ai",
      handoffs=[web_agent],
      tools=[
        planner_agent.as_tool(
          tool_name="planner_tool",
          tool_description="specialist in planning"
        ),
        devops_agent.as_tool(
          tool_name="devops_tool",
          tool_description="specialist in devops"
        )
      ]
      )
  mobile_agent=Agent(
    name="mobile agent",
    instructions="You are a mobile agent. Your sole responsibility is to answer questions strictly related to mobile query.",
    model=MODEL,
    handoff_description="specialist in any type of query regarding mobile",
    handoffs=[agentic_ai_agent]
  )

  @function_tool
  def draft_agreement(agreement:str):
      '''
      return agreement 
      '''

      agreement="this is the agreement tool"
      return agreement

  @function_tool
  def save_agreement(filename="agreement.txt"):
      """
      Calls draft_agreement and saves the agreement to a file.
      """
      agreement = draft_agreement()
      with open(filename, 'w') as file:
          file.write(agreement)

  panacloud_agent=Agent(
      name="panacloud_agent",
      instructions = """
      You are a supervisor agent. Carefully read the user's prompt and delegate the task to the appropriate agent. 
      If the user wants to create an agreement,and call draft_agreement tool and print agreement variable .
      If suitable agent is not available, politely respond with, 'I am not responsible for this task.'
      """,
      model=MODEL,
      handoffs=[mobile_agent,agentic_ai_agent,web_agent],
      tools=[draft_agreement,save_agreement]

  )

  result=await Runner.run(
    starting_agent=panacloud_agent,
    input=prompt,
  )

  return {"response": f"{result.last_agent.name} : {result.final_output}"}


