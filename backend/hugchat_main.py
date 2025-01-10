from fastapi import FastAPI
from pydantic import BaseModel
from system_prompt import system_prompt
from hugchat import hugchat
from hugchat.login import Login
from hugchat.hugchat import MessageNode, Conversation
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

cookie_path_dir = "./cookies/"
sign = Login(EMAIL, PASSWORD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

try:
    chatbot.delete_all_conversations()
    print("All conversations removed successfully.")
except Exception as e:
    print(e)

chatbot.new_conversation(switch_to=True, system_prompt=system_prompt)

class GenRequest(BaseModel):
    query: str

@app.post("/")
async def generate_breakdown(request: GenRequest):
    message = chatbot.chat(request.query).wait_until_done()
    return message
