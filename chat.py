from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "user", "content": "Hey I am Souvik"},
        {"role": "assistant", "content": "Hello Souvik! How can I assist you today?"},
        {"role": "user", "content": "What is my name"}
    ]
)

print(response.choices[0].message.content)