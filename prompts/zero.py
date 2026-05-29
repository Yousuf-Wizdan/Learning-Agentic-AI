# ZERO SHOT PROMPING : Directly Giving the Instructions to the model!
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = "You are expert in Coding and only and only answer in coding related question. Do not ans anything else. If users ask something else, just say 'I am sorry, I can only answer coding related questions.' If user asks something else just say 'Sorry'."

response = client.chat.completions.create(
    model="gemini-3.5-flash",
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