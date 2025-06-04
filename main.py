import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

@cl.on_chat_start
async def chat_start():
    await cl.Message("Hello! This is a simple Question/Answer Chatbot created by Fatima.").send()
    await cl.Message("How can I help you?").send()

    """Setting up chat history when user connects"""
    cl.user_session.set("chat_history", [])
    

@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("chat_history") or []

    history.append({"role":"user", "content": message.content})

    prompt = "\n".join([f"{msg["role"]}:{msg["content"]}" for msg in history])

    try:
        response = model.generate_content(prompt)

        response_text = response.text if hasattr(response, "text") else " "

    except Exception as e:
        response_text = f"Error {str(e)}"

    await cl.Message(content=response_text).send()

    history.append({"role":"model", "content": response_text})

    cl.user_session.set("chat_history", history)