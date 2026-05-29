from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os
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