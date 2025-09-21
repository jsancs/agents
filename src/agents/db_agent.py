from pydantic_ai import Agent, DeferredToolRequests, RunContext
from pydantic import BaseModel
import asyncio


class GetHumanInTheLoopInput(BaseModel):
    """Input for getting more information"""

    question: str


class GetHumanInTheLoopOutput(BaseModel):
    """Response for getting more information"""

    answer: str


def build_agent() -> Agent:

    db_agent = Agent(
        model="gpt-4.1-mini",
        instructions=(
            "You are a database system admin.\n",
            "Use the available tools to achieve the task asked by the user.\n"
            "Every time you need extra info, use get_human_in_the_loop() tool to ask the user.",
        ),
        output_type=[str | DeferredToolRequests],
    )

    @db_agent.tool_plain()
    def read_row(id: str) -> None:
        return f"Row with id {id}: Name -> Agent"

    @db_agent.tool_plain(requires_approval=True)
    def delete_row(id: str) -> None:
        return f"Row with id {id} deleted"

    @db_agent.tool
    async def get_human_in_the_loop(
        _: RunContext[GetHumanInTheLoopInput], question: str
    ) -> GetHumanInTheLoopOutput:
        input_str = await asyncio.to_thread(input, f"'{question}': ")
        return GetHumanInTheLoopOutput(answer=input_str)

    return db_agent
