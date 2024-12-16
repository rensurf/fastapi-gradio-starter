import os

import gradio as gr
from api import router
from dotenv import load_dotenv
from fastapi import FastAPI
from ui import create_interface

load_dotenv()

app = FastAPI()
app.include_router(router)


def create_app() -> FastAPI:
    interface = create_interface()
    demo = gr.mount_gradio_app(app, interface, path="/")

    return demo


demo = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
