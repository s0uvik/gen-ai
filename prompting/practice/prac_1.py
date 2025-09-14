from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are an AI assistant. Always respond in valid JSON format:
{
  "role": "assistant",
  "content": "your response here"
}
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    query = input(">>> ")

    if query.lower() in ["exit", "quit", "q"]:
        print("Goodbye! 👋")
        break

    if not query:
        print("⚠️ Empty input. Please type something.")
        continue

    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        response_format={"type": "json_object"},
        messages=messages,
    )

    content = response.choices[0].message.content

    try:
        parsed_content = json.loads(content)["content"]
    except (json.JSONDecodeError, KeyError):
        parsed_content = content

    messages.append({"role": "assistant", "content": parsed_content})
    print(f"🤖-> {parsed_content}")
