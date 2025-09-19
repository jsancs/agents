import asyncio
from dataclasses import dataclass

from pydantic_ai import Agent
from pydantic_graph import BaseNode, End, Graph, GraphRunContext
from dotenv import load_dotenv
from .models.agent_enum import AgentEnum

from .agents import build_bank_agent, build_db_agent, build_orchestration_agent


load_dotenv()


@dataclass
class GraphDeps:
    query: str
    orchestration_agent: Agent
    db_agent: Agent
    bank_agent: Agent


@dataclass
class BankManagerNode(BaseNode[None, None, str]):
    query: str

    async def run(self, ctx: GraphRunContext) -> End[str]:
        result = await ctx.deps.bank_agent.run(ctx.deps.query)
        # print(result.output)

        return End(result.output)


@dataclass
class DBManagerNode(BaseNode[None, None, str]):
    query: str

    async def run(self, ctx: GraphRunContext) -> End[str]:
        result = await ctx.deps.db_agent.run(ctx.deps.query)
        # print(result.output)

        return End(result.output)


@dataclass
class MyNode(BaseNode[None, None, str]):

    async def run(
        self, ctx: GraphRunContext
    ) -> BankManagerNode | DBManagerNode | End[str]:
        result = await ctx.deps.orchestration_agent.run(ctx.deps.query)

        parsed_agent = result.output.value
        print("Selected agent: ", parsed_agent)

        match parsed_agent:
            case AgentEnum.BANK_AGENT:
                return BankManagerNode(query=ctx.deps.query)
            case AgentEnum.DB_AGENT:
                return DBManagerNode(query=ctx.deps.query)
            case _:
                return End(parsed_agent)


async def main():
    user_query = input("Your query: ")

    graph = Graph(nodes=[MyNode, BankManagerNode, DBManagerNode])
    deps = GraphDeps(
        query=user_query,
        orchestration_agent=build_orchestration_agent(),
        bank_agent=build_bank_agent(),
        db_agent=build_db_agent(),
    )
    result = await graph.run(start_node=MyNode(), deps=deps)
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
