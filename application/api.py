import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter
from llm import llm_service
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    text: str
    status: str
    model: Optional[str] = None


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    prompt = (
        f"{request.system_prompt}\n\n{request.message}"
        if request.system_prompt
        else request.message
    )

    result = await llm_service.generate(
        prompt=prompt, temperature=os.getenv("TEMPERATURE", 0.5)
    )
    return ChatResponse(**result)
