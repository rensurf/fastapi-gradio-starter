import os
from typing import Dict, List, Tuple

import gradio as gr
from llm import llm_service


def create_interface() -> gr.Blocks:
    chat_history: List[Dict[str, str]] = []

    async def handle_chat(message: str, history: str) -> Tuple[str, str]:
        result = await llm_service.generate(
            prompt=message,
            history=chat_history,
            temperature=os.getenv("TEMPERATURE", 0.5),
        )

        chat_history.append({"role": "user", "content": message})
        if result["status"] == "success":
            chat_history.append({"role": "assistant", "content": result["text"]})

        display_history = "\n\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in chat_history]
        )

        return display_history

    with gr.Blocks() as interface:
        gr.Markdown("# LLM Chat Interface")

        with gr.Row():
            with gr.Column():
                message = gr.Textbox(
                    label="Message", placeholder="Enter your message here...", lines=3
                )
                submit = gr.Button("Send")

            with gr.Column():
                chat_display = gr.Textbox(label="Chat History", lines=20)

        submit.click(
            fn=handle_chat,
            inputs=[message, chat_display],
            outputs=[chat_display],
        )

    return interface
