import asyncio

from ollama import AsyncClient


async def test_ollama():
    try:
        client = AsyncClient(host="http://localhost:11434")
        response = await client.chat(
            model="elyza:jp8b",
            messages=[{"role": "user", "content": "Hello, how are you?"}],
            options={"temperature": 0.5},
        )
        print(f"Test response: {response}")
    except Exception as e:
        print(f"Ollama test error: {str(e)}")


asyncio.run(test_ollama())
