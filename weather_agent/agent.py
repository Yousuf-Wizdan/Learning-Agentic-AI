# Chain-Of-Thought Prompting: It is a prompting technique where you encourage an AI model to reason through a problem step by step before giving the final answer.

from openai import OpenAI
from dotenv import load_dotenv

import requests
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY")
)

def get_weather(city: str):
    url = f"http://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is: {response.text}"

    return "Sorry, I couldn't fetch the weather information."

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = """ 

You are an AI assistant that solves problems using a structured reasoning process.

You must ALWAYS respond with exactly one valid JSON object.

You can also call a tool if required from the list of available tools.

For every tool call wait for the OBSERVE step which is

The JSON schema is:

{
  "step": "PLAN" | "OUTPUT" | "TOOL",
  "tool": "string", // only for TOOL steps
  "input": "string", // only for TOOL steps
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
11. After a TOOL step, the system will provide the tool result.
12. Use the tool result to continue reasoning.
13. Never generate an OBSERVE step yourself.

Behavior:

- When a new user request arrives, begin with a PLAN step.
- During PLAN steps, think about what information is needed, what calculations must be performed, and what approach should be taken.
- Do not provide the final answer during PLAN steps.
- Once all necessary planning is complete, return an OUTPUT step containing the final answer.

Available Tools:
- get_weather(city): Takes city name as input string and returns the weather info about that city.

Examples:

Example 1:
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

Example 2:
    User: What is the weather in Jhansi?

    Assistant:
    {"step":"TOOL", "tool": "get_weather", "input":"Jhansi"}

    Assistant:
    {"step":"OBSERVE", "tool": "get_weather", "output":"The temperature of Jhansi is sunny with 34 C"}

    Assistant:
    {"step":"PLAN","content":"Review the weather information returned by the tool."}

    Assistant:
    {"step":"PLAN","content":"Determine the key details to include in the response, such as temperature and conditions."}

    Assistant:
    {"step":"OUTPUT","content":"The current weather in Jhansi is sunny with a temperature of 34°C."}

"""

print("\n\n\n")

message_history = [
    {"role" : "system", "content" : SYSTEM_PROMPT},
]

while True:
    user_input = input("👉 ")
    message_history.append({"role" : "user" , "content" : user_input})

    while True:
        response = client.chat.completions.create(
            model="mistral-small-latest",
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

            message_history.append({
                "role": "user",
                "content": "Continue reasoning."
            })
        
        elif step == "TOOL":
            tool_name = parsed_result["tool"]
            tool_input = parsed_result["input"]

            tool_response = available_tools[tool_name](tool_input)

            print("🔧", f"Calling tool: {tool_name}({tool_input}) = {tool_response}")

            # Store tool call
            message_history.append({
                "role": "assistant",
                "content": raw_results
            })

            # Give result back to model
            message_history.append({
                "role": "user",
                "content": f"Tool result: {tool_response}"
            })


        elif step == "OUTPUT":
            print("✅", parsed_result["content"])
            break

print("\n\n\n")

# 👉 What is the weather of banglore ?
# 🔧 Calling tool: get_weather(Bangalore) = The weather in Bangalore is: Patchy light rain +28°C
# 🧠 Review the weather information returned by the tool for Bangalore.
# 🧠 Determine the key details to include in the response, such as temperature and weather conditions.
# ✅ The current weather in Bangalore is patchy light rain with a temperature of 28°C.

# 👉 What is the weather of Delhi , Jhansi , Chandigarh and New York ?
# 🔧 Calling tool: get_weather(Delhi) = The weather in Delhi is: Sunny +40°C
# 🔧 Calling tool: get_weather(Jhansi) = The weather in Jhansi is: Moderate rain at times +40°C
# 🔧 Calling tool: get_weather(Chandigarh) = The weather in Chandigarh is: Sunny +39°C
# 🔧 Calling tool: get_weather(New York) = The weather in New York is: Sunny +12°C
# 🧠 Review the weather information for all four cities: Delhi, Jhansi, Chandigarh, and New York.
# 🧠 Organize the weather details for each city into a structured format for the final output.
# ✅ Here are the current weather conditions for the requested cities:

# - **Delhi**: Sunny, 40°C
# - **Jhansi**: Moderate rain at times, 40°C
# - **Chandigarh**: Sunny, 39°C
# - **New York**: Sunny, 12°C




    
    

