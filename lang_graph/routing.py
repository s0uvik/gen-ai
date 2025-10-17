from openai import OpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal

load_dotenv()


client = OpenAI()


class ClassifyMessages(BaseModel):
    is_coding_question: bool


class CodeAccuracyMessages(BaseModel):
    accuracy_percentage: str


# state
class State(TypedDict):
    user_query: str
    llm_response: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None


# tools
def classify_message(state: State):
    query = state["user_query"]

    SYSTEM_PROMPT = """ 
        You are an AI assistant. Your job is to detect if the user's query is
        related to coding question or not.
        Return the response in specified JSON boolean only.
        """

    llm_result = client.beta.chat.completions.parse(
        response_format=ClassifyMessages,
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    is_coding_question = llm_result.choices[0].message.parsed.is_coding_question
    state["is_coding_question"] = is_coding_question

    return state


def routing(state: State) -> Literal["general_query_resolver", "coding_query_resolver"]:

    is_coding_question = state["is_coding_question"]

    if is_coding_question:
        return "coding_query_resolver"
    else:
        return "general_query_resolver"


def general_query_resolver(state: State):

    query = state["user_query"]

    SYSTEM_PROMPT = """ 
        You are an helpful AI assistant who is specialized in resolving user query.
        """

    llm_result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    llm_response = llm_result.choices[0].message.content
    state["llm_response"] = llm_response

    return state


def coding_query_resolver(state: State):

    query = state["user_query"]

    SYSTEM_PROMPT = """ 
        You are an helpful Coding AI assistant who is specialized in resolving user coding query.
        """

    llm_result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    llm_response = llm_result.choices[0].message.content
    state["llm_response"] = llm_response

    return state


def accuracy_checker(state: State):
    query = state["user_query"]
    llm_result = state["llm_response"]

    SYSTEM_PROMPT = f""" 
        You are an AI assistant for checking code accuracy. return accuracy of code in percentage.

        User query: {query}
        LLM Results: {llm_result}
        """

    llm_result = client.beta.chat.completions.parse(
        response_format=CodeAccuracyMessages,
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    accuracy_percentage = llm_result.choices[0].message.parsed.accuracy_percentage
    state["accuracy_percentage"] = accuracy_percentage

    return state


graph_builder = StateGraph(State)

# define Nodes
graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("routing", routing)
graph_builder.add_node("general_query_resolver", general_query_resolver)
graph_builder.add_node("coding_query_resolver", coding_query_resolver)
graph_builder.add_node("accuracy_checker", accuracy_checker)

# edges
graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", routing)

graph_builder.add_edge("general_query_resolver", END)

graph_builder.add_edge("coding_query_resolver", "accuracy_checker")
graph_builder.add_edge("accuracy_checker", END)

graph = graph_builder.compile()


def main():
    user_query = input(">>")

    state: State = {
        "user_query": user_query,
        "llm_response": None,
        "accuracy_percentage": None,
        "is_coding_question": None,
    }

    response = graph.invoke(state)

    print(response)


main()
