import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

class TempOutput(BaseModel):
    response: str
    isBelow26: bool

father_guard = Agent(
    name="Father Guard",
    instructions="If temperature is below 26C, set isBelow26=True else False.",
    output_type=TempOutput
)

@input_guardrail
async def father_guardrail(ctx, agent, input):
    result = await Runner.run(father_guard, input, run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(output_info=result.final_output.response, tripwire_triggered=result.final_output.isBelow26)

child_agent = Agent(name="Child", instructions="You are a child who wants to play outside.", input_guardrails=[father_guardrail])

async def main():
    try:
        result = await Runner.run(child_agent, "The temperature is 24C", run_config=config)
        print("Child allowed:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("LOGS -> Guardrail Triggered: Father stopped child from going outside!")

if __name__ == "__main__":
    asyncio.run(main())
