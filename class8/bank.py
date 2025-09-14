import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class BankAccount(BaseModel):
    account_number: str
    customer_name: str
    account_balance: float
    account_type: str

bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="savings"
)

@function_tool
def get_bank_info(wrapper: RunContextWrapper[BankAccount]):
    return f"Customer {wrapper.context.customer_name} has {wrapper.context.account_type} account with balance {wrapper.context.account_balance} PKR."

bank_agent = Agent(
    name="Bank Agent",
    instructions="Always call the tool to provide bank account details.",
    tools=[get_bank_info]
)

async def main():
    result = await Runner.run(
        bank_agent,
        "Can you tell me account details?",
        run_config=config,
        context=bank_account
    )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
