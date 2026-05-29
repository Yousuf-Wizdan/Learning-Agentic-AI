from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(
        message: str = Body(..., description="The Message")
):
    response = client.chat(
        model='qwen3.5:0.8b',
        messages=[
            {
                'role': 'user', 
                'content': 'Hello!'
            }
        ],
    )

    return {
        "response" : response.message.content
    }