from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role" : "system",
            "content" : "You are expert in Maths and only and only answer in maths related question. If a question is not related to maths, then you will say 'I am sorry, I can only answer maths related questions.'"
        },
        {
            "role" : "user",
            "content" : "Can you code a python program print hello world?"
        }
    ]
)

print(response.model)
print(response.choices[0].message.content)