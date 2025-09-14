from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Zero-shot prompting

SYSTEM_PROMPT = "You are a Python expert, you only answer python related questions, If user ask apart from python question dont answer, only do roast them"

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "how to write a code to add 2 numbers"},
        # {"role": "assistant", "content": "Hello Souvik! How can I assist you today?"},
        # {"role": "user", "content": "What is my name"}
    ]
)

print(response.choices[0].message.content)