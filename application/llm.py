import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ollama import AsyncClient


class LLMService(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        temperature: float,
    ) -> Dict[str, Any]:
        raise NotImplementedError


class OllamaService(LLMService):
    def __init__(self):
        self.model = os.getenv("MODEL_NAME", "elyza:jp8b")
        self.client = AsyncClient(
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )

    async def generate(
        self, prompt: str, history: List[Dict[str, str]], temperature: float = 0.5
    ) -> Dict[str, Any]:
        try:
            messages = history + [{"role": "user", "content": prompt}]
            response = await self.client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature},
            )
            print(f"Debug result: {response}")

            return {
                "text": response["message"]["content"],
                "model": self.model,
                "status": "success",
            }

        except Exception as e:
            return {"text": f"Error: {str(e)}", "status": "error"}


llm_service = OllamaService()
