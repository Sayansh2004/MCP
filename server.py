from fastmcp import FastMCP


mcp=FastMCP("add and subtract numbers")


@mcp.tool
def add(a:int,b:int)->int:
    """Use this tool to add two numbers together."""
    return a+b

@mcp.tool
def subtract(a:int,b:int)->int:
    """Use this tool to subtract one number from another."""
    return a-b

if __name__=="__main__":
    mcp.run()

