from pydantic_ai import Agent, DeferredToolRequests


def build_agent() -> Agent:

    db_agent = Agent(
        model="gpt-4.1-mini",
        instructions="You are a database system admin.",
        output_type=[str | DeferredToolRequests],
    )

    @db_agent.tool_plain()
    def read_row(id: str) -> None:
        return f"Row with id {id}: Name -> Agent"

    # @db_agent.tool_plain(requires_approval=True)
    # def delete_row(id: str) -> None:
    #     return f"Row with id {id} deleted"

    return db_agent
