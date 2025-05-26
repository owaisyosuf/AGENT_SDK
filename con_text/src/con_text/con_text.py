from agents import Agent, Runner, AsyncOpenAI,set_default_openai_api,set_default_openai_client,set_tracing_disabled, function_tool,RunContextWrapper
from dotenv import load_dotenv
import asyncio
import os
from dataclasses import dataclass

load_dotenv()

set_tracing_disabled(True)
set_default_openai_api('chat_completions')

api_key= os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("api key is not found")

external_client=AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)

MODEL="gemini-2.0-flash"

# @dataclass
# class UserInfo:  
#     name: str
#     uid: int

# # A tool function that accesses local context via the wrapper
# @function_tool
# async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
#     return f"User {wrapper.context.name} is 47 years old"

# async def main():
#     # Create your context object
#     user_info = UserInfo(name="John", uid=123)  

#     # Define an agent that will use the tool above
#     agent = Agent[UserInfo](  
#         name="Assistant",
#         instructions="You are a helpful assistant. Use the fetch_user_age tool to return the age when the user provides their name.",
#         tools=[fetch_user_age],
#         model=MODEL
#     )

#     # Run the agent, passing in the local context
#     result = await Runner.run(
#         starting_agent=agent,
#         input="What is the age of the user?",
#         context=user_info,
#     )

#     print(result.final_output)  # Expected output: The user John is 47 years old.

# if __name__ == "__main__":
#     asyncio.run(main())
# @dataclass
# class UserInfo1:
#     name: str
#     uid: int
#     location: str = "Pakistan"

# @function_tool
# async def fetch_user_age(wrapper: RunContextWrapper[UserInfo1]) -> str:
#     '''Returns the age of the user.'''
#     return f"User {wrapper.context.name} is 30 years old"

# @function_tool
# async def fetch_user_location(wrapper: RunContextWrapper[UserInfo1]) -> str:
#     '''Returns the location of the user.'''
#     return f"User {wrapper.context.name} is from {wrapper.context.location}"

# async def main():
#     user_info = UserInfo1(name="Muhammad Qasim", uid=123 , location="karachi")

#     agent = Agent[UserInfo1](
#         name="Assistant",
#         tools=[fetch_user_age,fetch_user_location],
#         model=MODEL
#     )

#     result = await Runner.run(
#         starting_agent=agent,
#         input="What is the age of the user? current location of his/her?",
#         context=user_info,
#     )

#     print(result.final_output)
#     # The user John is 47 years old.

# if __name__ == "__main__":
#     asyncio.run(main())

@dataclass
class user_info:
    name:str
    age:int
    address:str="karachi"

@function_tool
async def get_user_name(wrapper:RunContextWrapper[user_info]) -> str:
    '''Returns the age of the user.'''
    f"user name is{wrapper.context.name} and he/she live in {wrapper.context.address}" 
@function_tool
async def get_user_age(wrapper:RunContextWrapper[user_info])->str:
    '''return user name with age and address'''
    f"user name is {wrapper.context.name} user age is {wrapper.context.age} and he located at {wrapper.context.address}"

async def main():
    user_data=user_info(name="owais", age=36)

    agent=Agent(
        name="assistant",
        # instructions="return user info using get_user_name and get_user_age tool",
        tools=[get_user_name,get_user_age],
        model=MODEL
    )

    result=await Runner.run(
        agent,
        "what is the age",
        context=user_data
    )
    print(result.final_output)

asyncio.run(main())