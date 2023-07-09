from fastapi import FastAPI, Body, HTTPException, Request
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import openai
from typing import Optional
import requests
import os

app=FastAPI()

load_dotenv()
openai.api_key = os.getenv('SECRET_KEY')

class Item(BaseModel):
    entry: list

@app.post("/webhook/")
async def webhook_whatsapp(item: Item, request: Request, hub_verify_token: Optional[str] = None, hub_challenge: Optional[str] = None):
    if hub_verify_token == "HolaFaby":
        return {"hub.challenge": hub_challenge}
    else:
        return {"Error": "Error de autentificacion."}
    
    data = item.dict()

    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']

    if mensaje is not None:
        import openai
        model_engine = "text-davinci-003"
        prompt = mensaje
        completion = openai.Completion.create(engine=model_engine,
                                            prompt=prompt,
                                            max_tokens=1024,
                                            n=1,
                                            stop=None,
                                            temperature=0.7)
        respuesta=""
        for choice in completion.choices:
            respuesta=respuesta+choice.text.strip()
            print(f"Response: %s" % choice.text.strip())
        
        respuesta=respuesta.replace("\\n","\\\n")
        respuesta=respuesta.replace("\\","")
        
        with open("texto.txt", "w") as f:
            f.write(respuesta)
        
        return {"status": "success"}