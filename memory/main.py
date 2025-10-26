from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
import json

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration for mem0 + Qdrant
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "api_key": OPENAI_API_KEY,
        "model": "text-embedding-3-small",
    },
    "llm": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": "http://127.0.0.1:6333",  # ✅ local Qdrant server
            "collection_name": "souvik_memory",  # optional but useful
        },
    },
}

# Initialize mem0 memory client
mem_client = Memory.from_config(config)


# Simple chat loop
def chat():
    while True:
        query = input(">> ")

        all_memories = mem_client.get_all(user_id="souvik")

        # this will be a array
        relevant_memories = mem_client.search(query=query, user_id="souvik")
        memories = [
            f"id: {mem.get("id")} memory: {mem.get("memory")}"
            for mem in relevant_memories.get("results")
        ]
        # print(memories)
        SYSTEM_PROMPT = f"""
        You are a memories aware assistant, response to user with context. You have fast memories.

        Memories of the user:{json.dumps(memories)}      
        """

        result = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )

        response = result.choices[0].message.content
        print(response)

        # Store in memory
        messages = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": response},  # ✅ fixed wrong key
        ]

        mem_client.add(messages, user_id="souvik")


chat()
