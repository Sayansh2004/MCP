from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

from langgraph.prebuilt import create_react_agent
load_dotenv()

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)

client=MultiServerMCPClient(
    {
        "knowledge_assistant":{
            "url":"http://localhost:8000",
            "transport":"sse"
        }
    }
)
agent=None

async def initialise_agent():
    
    tools=await client.get_tools("knowledge_assistant")
    systemp_prompt="""
    You are a helpful personal assistant that helps users manage their notes by :
    -saving new notes
    -retrieving existing notes
    -updating existing notes
    -researching on a specific topic by retrieving relevant notes

    You have access to these tools to interact with the knowledge base

    STRICT RULES:
    -ONLY use the provided tools to interact with the knowledge base
    -NEVER attempt to access the knowledge base without using the provided tools
    -when fetched notes , represent them in a concise manner by only including the title and description of the note and author and everything
    - Always confirm whenever a new note is created or updated
     - If user asks something outside of the scope of managing notes, respond with "I can only help with managing notes. Please ask me to save, retrieve, update, or research notes."
"""

    agent=create_react_agent(llm,tools,prompt=SystemMessage(content=systemp_prompt))
    

async def run_agent(user_input):
    global agent

    if agent is None:
        await initialise_agent()

    response=await agent.ainvoke([HumanMessage(content=user_input)])
    return response.content
