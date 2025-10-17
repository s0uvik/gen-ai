from openai import OpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# State
class State(TypedDict):
    query: str
    llm_results: str | None


# Node
def chat_bot(state: State):
    # llm call
    llm_results = client.chat.completions.create(
        model="gpt-4.1", messages=[{"role": "user", "content": state["query"]}]
    )

    results = llm_results.choices[0].message.content
    state["llm_results"] = results

    return state


# Edge
graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()


def main():
    query = input(">>")

    state = {"query": query, "llm_results": None}

    graph_results = graph.invoke(state)

    print(graph_results)


main()
