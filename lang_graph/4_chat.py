from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model(model_provider="openai", model="gpt-4.1")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()


def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer


def main():
    DB_URI = "mongodb://admin:admin@localhost:27017"
    config = {"configurable": {"thread_id": "1"}}
    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:

        graph_with_mongo = compile_graph_with_checkpointer(checkpointer)

        query = input(">>")

        # this create a fresh new state
        result = graph_with_mongo.invoke(
            {"messages": [{"role": "user", "content": query}]}, config
        )
        # after this deleted the state
        ai_message = result["messages"][-1].content
        print(ai_message)


main()
