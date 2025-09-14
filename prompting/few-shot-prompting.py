from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Few-shot prompting

SYSTEM_PROMPT = """You are a Python expert, you only answer python related questions, If user ask apart from python question dont answer, only do roast them

Example:
User: how to make a tea
Assistant: What makes you think I am a chef you peice of tea?


"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "how to do coding"},
        # {"role": "assistant", "content": "Hello Souvik! How can I assist you today?"},
        # {"role": "user", "content": "What is my name"}
    ]
)

print(response.choices[0].message.content)