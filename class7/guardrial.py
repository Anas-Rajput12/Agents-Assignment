import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

class StudentOutput(BaseModel):
    response: str
    isChangeClassTiming: bool

class_timing_guard = Agent(
    name="Class Timing Guard",
    instructions="If user talks about changing class timings, set isChangeClassTiming=True else False.",
    output_type=StudentOutput
)

@input_guardrail
async def timing_guardrail(ctx, agent, input):
    result = await Runner.run(class_timing_guard, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(output_info=result.final_output.response, tripwire_triggered=result.final_output.isChangeClassTiming)

student_agent = Agent(name="Student", instructions="You are a student agent.", input_guardrails=[timing_guardrail])

async def main():
    try:
        result = await Runner.run(student_agent, "I want to change my class timings", run_config=config)
        print("Student request accepted:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("LOGS -> Guardrail Triggered: Changing class timings is not allowed!")

if __name__ == "__main__":
    asyncio.run(main())
