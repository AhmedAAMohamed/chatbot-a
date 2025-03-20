from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import sys

# Configure logging
print("Starting backend application...")
print(f"Python version: {sys.version}")

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Changed to more widely available model

# Print debug info (without exposing the full API key)
print(f"OpenAI API Key configured: {'Yes' if OPENAI_API_KEY else 'No'}")
print(f"OpenAI Model: {OPENAI_MODEL}")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="Chatbot-A API", version="1.0.0")

# Configure CORS - allowing requests from any origin for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat models
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (system, user, assistant)")
    content: str = Field(..., description="Content of the message")
    
class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages in the conversation")
    model: Optional[str] = Field(None, description="OpenAI model to use (defaults to gpt-4)")
    temperature: Optional[float] = Field(0.7, description="Temperature for response generation")
    
class ChatResponse(BaseModel):
    message: str = Field(..., description="The assistant's response")
    role: str = Field("assistant", description="Role of the message sender")
    created_at: datetime = Field(default_factory=datetime.now)

# Root endpoint for basic testing
@app.get("/", status_code=200)
async def root():
    return {"status": "API is running", "version": app.version}

# Chat endpoint - removed authentication requirement
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        print(f"Received chat request with {len(request.messages)} messages")
        
        if not OPENAI_API_KEY:
            print("ERROR: OpenAI API key not configured")
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            )
        
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Add system message if not already present
        if not any(msg["role"] == "system" for msg in messages):
            messages.insert(0, {
                "role": "system",
                "content": "You are a helpful AI assistant developed for the Chatbot-A project."
            })
        
        model = request.model or OPENAI_MODEL
        print(f"Using model: {model}")
        
        try:
            print("Calling OpenAI API...")
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=request.temperature
            )
            
            response_content = completion.choices[0].message.content
            print(f"Received response from OpenAI ({len(response_content)} chars)")
            
            return {
                "message": response_content,
                "role": "assistant",
                "created_at": datetime.now()
            }
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
            
    except Exception as e:
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health", status_code=200)
async def health_check():
    return {
        "status": "healthy", 
        "version": app.version, 
        "openai_api_configured": bool(OPENAI_API_KEY),
        "model": OPENAI_MODEL
    }

# Export app for Vercel
app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 