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
    
@cl.on_message
async def handle_message(message: cl.Message):

    prompt = message.content

    response = model.generate_content(prompt)

    response_text = response.text if hasattr(response, "text") else " "

    await cl.Message(content=response_text).send()


port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    cl.run(host="0.0.0.0", port=port)