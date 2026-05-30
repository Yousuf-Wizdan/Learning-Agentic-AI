from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

def get_weather(city: str):
    url = f"http://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is: {response.text}"

    return "Sorry, I couldn't fetch the weather information."

def main():
    user_query = input("> ")
    
    response =client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {
                "role" : "user",
                "content": user_query
            }
        ]
    )

    print(f"🤖: {response.choices[0].message.content}")

# main()
# print(get_weather("Jhansi"))