import asyncio
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext
from dotenv import load_dotenv

from .agents.orchestration_agent import orchestration_agent


load_dotenv()


@dataclass
class GraphDeps:
    query: str


@dataclass
class MyNode(BaseNode[None, None, str]):

    async def run(self, ctx: GraphRunContext) -> End[str]:
        result = await orchestration_agent.run(ctx.deps.query)

        parsed_agent = result.output.value
        print("Selected agent: ", parsed_agent)
        return End(parsed_agent)


async def main():
    user_query = input("Your query: ")

    graph = Graph(nodes=[MyNode])
    result = await graph.run(start_node=MyNode(), deps=GraphDeps(query=user_query))
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
