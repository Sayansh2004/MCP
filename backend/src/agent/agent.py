from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

client = MultiServerMCPClient(
    {
        "knowledge_assistant": {
            "url": "http://localhost:8000/mcp",
            "transport": "sse"
        }
    }
)

agent = None


async def initialise_agent():
    global agent 
    tools = await client.get_tools()  

    system_prompt = """
    You are a helpful personal assistant and always greet user for the first time they interact with you. You help users manage their notes by:
    - Saving new notes
    - Retrieving existing notes
    - Updating existing notes
    - Researching on a specific topic by retrieving relevant notes

    You have access to these tools to interact with the knowledge base.

    STRICT RULES:
    - ONLY use the provided tools to interact with the knowledge base
    - NEVER attempt to access the knowledge base without using the provided tools
    - When fetching notes, represent them in a concise manner by only including the title, description, author, and any other relevant fields
    - Always confirm whenever a new note is created or updated
    - If the user asks something outside of the scope of managing notes, respond with:
      "I can only help with managing notes. Please ask me to save, retrieve, update, or research notes."
    """

    agent = create_react_agent(llm, tools, prompt=SystemMessage(content=system_prompt))


async def run_agent(user_input: str) -> str:
    global agent

    if agent is None:
        await initialise_agent()

    response = await agent.ainvoke({"messages": [HumanMessage(content=user_input)]})

    return response["messages"][-1].content


async def main():
    print("Knowledge Assistant ready. Type 'exit' or 'quit' to stop.\n")

  
    await initialise_agent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = await run_agent(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())