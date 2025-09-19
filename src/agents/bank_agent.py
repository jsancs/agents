from pydantic_ai import Agent


bank_agent = Agent(
    model="gpt-4.1-mini",
    instructions="your are a bank manager.",
    output_type=[str],
)


@bank_agent.tool
def get_balance() -> None:
    return f"Balance is 123€"
