# FEW SHOT PROMPTING : Giving the Instructions along with some examples to the model!

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

SYSTEM_PROMPT = """

You are expert in Coding and only and only answer in coding related question. Do not ans anything else. If users ask something else, just say 'I am sorry, I can only answer coding related questions.' If user asks something else just say 'Sorry'.

EXAMPLES:
Q: Can you explain the a + b whole square?
A: Sorry, I can only answer coding related questions.

Q: Hey, Write a code in python for adding two numbers.
A: def add(a, b):
    return a + b

"""

response = client.chat.completions.create(
    model="gemma-4-31b-it-20260402:free",
    messages=[
        {
            "role" : "system",
            "content" : SYSTEM_PROMPT
        },
        {
            "role" : "user",
            "content" : "Hey can you explain a + B whole square"
        }
    ]
)

# print(response.model)
print(response.choices[0].message.content)