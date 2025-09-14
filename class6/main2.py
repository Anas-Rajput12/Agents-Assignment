from agents import Agent, Runner, trace, function_tool
from connection import config
import asyncio
from dotenv import load_dotenv
# import chainlit as cl

load_dotenv()

@function_tool
def current_weather():
    return "Sunny"

@function_tool
def current_location():
    return "GH Sindh Karachi"



# 🔹 Poet Agent
poet_agent = Agent(
    name="poet_agent",
    instructions=(
        "Write a short poem of 2 stanzas about emotions, a story, or a dramatic act. "
        "Make it simple and creative."
    )
)

# 🔹 Analyst Agents
lyric_analyst = Agent(
    name="lyric_analyst",
    instructions="If the poem is about feelings or emotions, identify it as Lyric Poetry and explain why."
)

narrative_analyst = Agent(
    name="narrative_analyst",
    instructions="If the poem tells a story with events or characters, identify it as Narrative Poetry and explain why."
)

dramatic_analyst = Agent(
    name="dramatic_analyst",
    instructions="If the poem is written for performance or a character speaking, identify it as Dramatic Poetry and explain why."
)

# 🔹 Parent Agent
parent_agent = Agent(
    name="parent_agent",
    instructions=(
        "Read the poem. Decide whether it is Lyric, Narrative, or Dramatic Poetry. "
        "Send it to the correct analyst agent for explanation."
    ),
    handoffs=[poet_agent, lyric_analyst, narrative_analyst, dramatic_analyst],
    tools=[current_weather, current_location]
)


async def main():
        with trace("Lyrics Agents"):
            result = await Runner.run(
                parent_agent, 
                """
                    The sun sets low, painting skies with gold,  
A quiet story in the evening told
                """, 
                run_config=config
            )
            print(result.final_output)
            print("Last Agent ==> ", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())