# ZERO SHOT PROMPING : Directly Giving the Instructions to the model!
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

SYSTEM_PROMPT = "You are expert in Coding and only and only answer in coding related question. Do not ans anything else. If users ask something else, just say 'I am sorry, I can only answer coding related questions.' If user asks something else just say 'Sorry'."

response = client.chat.completions.create(
    model="gemma-4-31b-it-20260402:free",
    messages=[
        {
            "role" : "system",
            "content" : SYSTEM_PROMPT
        },
        {
            "role" : "user",
            "content" : "Write me hello world in rust program?"
        }
    ]
)

print(response.model)
print(response.choices[0].message.content)