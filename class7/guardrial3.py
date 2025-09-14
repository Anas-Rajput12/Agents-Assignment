import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

class GateOutput(BaseModel):
    response: str
    isOtherSchool: bool

gatekeeper_guard = Agent(
    name="Gatekeeper Guard",
    instructions="If student is from 'XYZ School' set isOtherSchool=False else True.",
    output_type=GateOutput
)

@input_guardrail
async def gatekeeper_guardrail(ctx, agent, input):
    result = await Runner.run(gatekeeper_guard, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(output_info=result.final_output.response, tripwire_triggered=result.final_output.isOtherSchool)

school_student = Agent(name="School Student", instructions="You are a student trying to enter school.", input_guardrails=[gatekeeper_guardrail])

async def main():
    try:
        result = await Runner.run(school_student, "I am from ABC School.", run_config=config)
        print("Student Allowed:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("LOGS -> Guardrail Triggered: Gatekeeper stopped student from other school!")

if __name__ == "__main__":
    asyncio.run(main())
