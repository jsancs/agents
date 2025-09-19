from pydantic_ai import Agent


def build_agent() -> Agent:
    bank_agent = Agent(
        model="gpt-4.1-mini",
        instructions="your are a bank manager.",
        output_type=[str],
    )

    @bank_agent.tool_plain
    def get_balance() -> None:
        return f"Balance is 123€"

    return bank_agent
