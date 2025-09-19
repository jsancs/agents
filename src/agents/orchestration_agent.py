from pydantic import BaseModel, Field
from pydantic_ai import Agent
from ..models import AgentEnum


def build_agent() -> Agent:
    orchestration_agent = Agent(
        model="gpt-4.1-mini",
        instructions=(
            "Your are an orchestration agent.\n",
            "Your goal is to identify which agent should be used next.\n",
            f"Options are: `{AgentEnum.BANK_AGENT}` or `{AgentEnum.DB_AGENT}`.\n",
            "Choose based on the user input question.",
        ),
        output_type=AgentEnum,
    )

    return orchestration_agent
