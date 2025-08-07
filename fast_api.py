import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

GEMINI_API_KEY = 'Enter Your own API-key'

genai.configure(api_key = GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

class ContentRequest(BaseModel):
    topic : str
    tone: str = 'informative'
    length : str = "medium"


@app.post("/generate")

def generate_content(req: ContentRequest):
    prompt = f"""
            Write a {req.length} piece of content on the topic: '{req.topic}'.
            The topic should be {req.tone}
            Make it creative, clear, and engaging and in simple language
        """
    
    try:
        response = model.generate_content(prompt)
        print(f"Generated content: {response.text}")
        return {"generate_content": response.text}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
