from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import openai
from typing import Optional
import requests
import os

app=FastAPI()

load_dotenv()

openai.api_key = os.getenv('SECRET_KEY')
TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

class Prompt(BaseModel):
    text: str = Field(min_lenght=10, max_lenght=100)

@app.get("/")
async def root():
    return {"message":"Hello World from Fabian"}

@app.get("/test")
async def root():
    return {"message":"this is test"}


@app.post('/chat')
def generate_response(prompt: Prompt):
    text_lenght = 1000
    gpt_model = "text-davinci-002"
    response = openai.Completion.create(
        engine=gpt_model,
        prompt=prompt.text,
        max_tokens=text_lenght,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response['choices'][0]['text']

    
@app.post("/webhook/")
async def process_webhook(data: dict = Body(...)):
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]
    text_lenght = 1000
    gpt_model = "text-davinci-002"
    response = openai.Completion.create(
        engine=gpt_model,
        prompt=text,
        max_tokens=text_lenght,
        n=1,
        stop=None,
        temperature=0.5
    )

    response_text = response.choices[0].text.strip()  # Get the response text

    requests.post(TELEGRAM_SEND_MESSAGE_URL, data={"chat_id": chat_id, "text": response_text})

    return {"ok": True}