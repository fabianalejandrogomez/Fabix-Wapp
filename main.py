from fastapi import FastAPI
import openai



app=FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World from Smurfcoders"}

@app.get("/test")
async def root():
    return {"message":"this is test"}

@app.get("/aplicar_openai", status_code=status.HTTP_200_OK, tags=["OpenAI"])
def get_all_fruits(pregunta: OPenAISchema):

    openai.api_key = "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"

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=pregunta.question,
    max_tokens=60
    )
    message = response.choices[0].text.strip()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message":message})

    
