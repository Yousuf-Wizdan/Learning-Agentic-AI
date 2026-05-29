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

RULE:
- Striclty follow the output in JSON format

Output Format:
{{
    "code" : "string" or null,
    "isCodingQuestion: : boolean
}}

EXAMPLES:
Q: Can you explain the a + b whole square?
A: {{
    "code" : null,
    "isCodingQuestion: : false
}}

Q: Hey, Write a code in python for adding two numbers.
A: {{
    "code" : "def add(a, b):\\n    return a + b",
    "isCodingQuestion: : true
}}

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
            "content" : "Hey write a code to add n numbers in js"
        }
    ]
)

# print(response.model)
print(response.choices[0].message.content)