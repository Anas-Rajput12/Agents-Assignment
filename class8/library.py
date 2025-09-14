import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool

library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)

@function_tool
def get_book_info(wrapper: RunContextWrapper[LibraryBook]):
    status = "available" if wrapper.context.is_available else "not available"
    return f"Book '{wrapper.context.book_title}' by {wrapper.context.author_name} is currently {status}."

book_agent = Agent(
    name="Library Agent",
    instructions="""
    You are a Library Agent.
    Never generate your own response.
    Always call the tool `get_book_info` to answer user queries.
    """,
    tools=[get_book_info]
)

async def main():
    result = await Runner.run(
        book_agent,
        "What about this book?",
        run_config=config,
        context=library_book
    )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
