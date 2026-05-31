import asyncio


async def run_agent(agent):
    while True:
        user_input=input("You : ")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting agent...")
            break
        response=await agent.arun(HumanMessage(content=user_input))