import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int

student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

@function_tool
def get_student_info(wrapper: RunContextWrapper[StudentProfile]):
    return f"Student {wrapper.context.student_name} (ID: {wrapper.context.student_id}) is in semester {wrapper.context.current_semester} with {wrapper.context.total_courses} courses."

student_agent = Agent(
    name="Student Agent",
    instructions="""
    You are a Student Agent. 
    Never generate your own response. 
    Always call the tool `get_student_info` to answer user queries.
    """,
    tools=[get_student_info]
)

async def main():
    result = await Runner.run(
        student_agent,
        "Who is this student?",
        run_config=config,
        context=student
    )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
