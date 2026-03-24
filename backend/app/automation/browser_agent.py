import asyncio
from browser_use import Agent
from langchain_ollama import ChatOllama

def run_browser_task(task_description: str) -> str:
    """
    Runs a browser automation task synchronously using asyncio.run.
    """
    async def _run():
        llm = ChatOllama(model="mistral")
        agent = Agent(task=task_description, llm=llm)
        result = await agent.run()
        
        # Result is an AgentHistoryList, we can check for errors
        if hasattr(result, "has_errors") and result.has_errors():
            return "Browser task finished but encountered some errors."
            
        final_result = result.final_result() if hasattr(result, "final_result") else ""
        if final_result:
            return f"Browser task completed: {final_result}"
            
        return "Browser task completed successfully."

    try:
        return asyncio.run(_run())
    except Exception as e:
        print("Browser Agent Error:", e)
        return f"Failed to complete browser task: {str(e)}"
