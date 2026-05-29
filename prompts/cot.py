# Chain-Of-Thought Prompting: It is a prompting technique where you encourage an AI model to reason through a problem step by step before giving the final answer.

from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

SYSTEM_PROMPT = """ 

You are an expert AI Assistant is resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

RULES:
- Strictly follow the given JSON output format
- Only run one step at a time.
- The sequence of the steps is START (where user gives an input), PLAN (That can be multiples times) and finally OUTPUT(which is going to be displayed to the user)

OUTPUT JSON Format:
   { "step" : "START" | "PLAN" | "OUTPUT" , "content" : "string" }

EXAMPLE:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step" : "PLAN" : "content" : "Seems like user is interested in maths problem"} 
PLAN: {"step" : "PLAN" : "content" : "I need to follow BODMAS rule to solve this problem"}
PLAN: {"step" : "PLAN" : "content" : "Yes, The BODMAS is the correct hing here"}
PLAN: {"step" : "PLAN" : "content" : "First we multuply 3 * 5 which is 15"}
PLAN: {"step" : "PLAN" : "content" : "Now the equation is 2 + 15 / 10"}
PLAN: {"step" : "PLAN" : "content" : "We must perfore division before addition, so we divide 15 by 10 which is 1.5"}
PLAN: {"step" : "PLAN" : "content" : "Now the equation is 2 + 1.5 which is 3.5"}
OUTPUT: {"step" : "OUTPUT" : "content" : "The answer is 3.5"}

"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b:free",
    response_format={ "type" : "json_object" },
    messages=[
        {
            "role" : "system",
            "content" : SYSTEM_PROMPT
        },
        {
            "role" : "user",
            "content" : "Hey write a code to add n numbers in java"
        },
        # Manually Keep Adding messages to the history based on the response from the model until you get the final output from the model with "step" : "OUTPUT"
        {
            "role" : "assistant",
            "content" : json.dumps({
                "step":"PLAN",
                "content":"User wants a Java program that adds n numbers. Need to decide input method (e.g., read n then numbers from console) and output sum. Provide full code with main method, using Scanner."
            })
        },
        {
            "role" : "assistant",
            "content" : json.dumps(
                {"step": "OUTPUT", "content": "Here is a simple Java program that reads an integer n from the console, then reads n numbers (as doubles) and prints their sum:\n\n```java\nimport java.util.Scanner;\n\npublic class AddNNumbers {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        \n        System.out.print(\"Enter how many numbers to add (n): \");\n        int n = scanner.nextInt();\n        \n        double sum = 0.0;\n        for (int i = 1; i <= n; i++) {\n            System.out.print(\"Enter number \" + i + \": \");\n            double num = scanner.nextDouble();\n            sum += num;\n        }\n        \n        System.out.println(\"The sum of the \" + n + \" numbers is: \" + sum);\n        \n        scanner.close();\n    }\n}\n```\n\n**Explanation**\n1. **Scanner** is used to read input from the console.\n2. The program first asks for `n`, the count of numbers to add.\n3. It then loops `n` times, prompting the user for each number and adding it to `sum`.\n4. After the loop, it prints the total sum.\n\nYou can compile and run it with:\n```\njavac AddNNumbers.java\njava AddNNumbers\n```"}
            )
        }
    ]
    

)

# print(response.model)
print(response.choices[0].message.content)