# Chain-Of-Thought Prompting: It is a prompting technique where you encourage an AI model to reason through a problem step by step before giving the final answer.

from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY")
)

SYSTEM_PROMPT = """ 

You are an AI assistant that solves problems using a structured reasoning process.

You must ALWAYS respond with exactly one valid JSON object.

The JSON schema is:

{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": "string"
}

Rules:

1. Return ONLY a JSON object.
2. Do NOT return markdown.
3. Do NOT use code blocks.
4. Do NOT add any text before or after the JSON.
5. The "content" field must always be a string.
6. Generate exactly one step per response.
7. The process must follow this order:
   START -> PLAN -> PLAN -> ... -> OUTPUT
8. Use as many PLAN steps as necessary.
9. When enough planning has been completed, return OUTPUT.
10. Never skip directly from START to OUTPUT unless the task is trivial.
11. The OUTPUT step must contain the final answer for the user.
12. Every response must be valid JSON that can be parsed using json.loads().

Behavior:

- When a new user request arrives, begin with a PLAN step.
- During PLAN steps, think about what information is needed, what calculations must be performed, and what approach should be taken.
- Do not provide the final answer during PLAN steps.
- Once all necessary planning is complete, return an OUTPUT step containing the final answer.

Example:

User: What is 2 + 5 / 10 - 2 * 10

Assistant:
{"step":"PLAN","content":"Interpret the arithmetic expression using order of operations."}

Assistant:
{"step":"PLAN","content":"Compute division: 5 / 10 = 0.5."}

Assistant:
{"step":"PLAN","content":"Compute multiplication: 2 * 10 = 20."}

Assistant:
{"step":"PLAN","content":"Substitute the results into the expression."}

Assistant:
{"step":"OUTPUT","content":"The answer is -17.5."}

"""

print("\n\n\n")

message_history = [
    {"role" : "system", "content" : SYSTEM_PROMPT},
]

user_input = input("👉 ")
message_history.append({"role" : "user" , "content" : user_input})

# Learned form the course
# while True:

    # response = client.chat.completions.create(
    #     model = "mistral-large-latest",
    #     response_format={ "type" : "json_object"},
    #     messages=message_history
    # )

    # raw_results = response.choices[0].message.content
    # message_history.append({"role" : "assistant" , "content" : raw_results})

    # parsed_result = json.loads(raw_results)

    # if(parsed_result.get("step") == "START"):
    #     print("🔥" , parsed_result.get("content"))
    #     continue

    # if(parsed_result.get("step") == "PLAN"):
    #     print("🧠" , parsed_result.get("content"))
    #     continue

    # if(parsed_result.get("step") == "OUTPUT"):
    #     print("✅" , parsed_result.get("content"))
    #     break

while True:
    response = client.chat.completions.create(
        model="mistral-large-latest",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_results = response.choices[0].message.content
    parsed_result = json.loads(raw_results)

    step = parsed_result["step"]

    if step == "PLAN":
        print("🧠", parsed_result["content"])

        message_history.append({
            "role": "assistant",
            "content": raw_results
        })

        # Important: add a user turn
        message_history.append({
            "role": "user",
            "content": "Continue reasoning."
        })

    elif step == "OUTPUT":
        print("✅", parsed_result["content"])
        break

print("\n\n\n")


# 👉 What is 2 + 5 / 10 - 2 * 10
# 🧠 Interpret the arithmetic expression respecting order of operations (PEMDAS/BODMAS).
# 🧠 First compute the division: 5 / 10 = 0.5.
# 🧠 Next compute the multiplication: 2 * 10 = 20.
# ✅ The result of 2 + 5 / 10 - 2 * 10 is -17.5.

    
    

