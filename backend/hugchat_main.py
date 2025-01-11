from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from system_prompt import system_prompt
from hugchat import hugchat
from hugchat.login import Login
# import os
# from dotenv import load_dotenv

app = FastAPI()

# load_dotenv()

# EMAIL = os.getenv("EMAIL")
# PASSWORD = os.getenv("PASSWORD")

# try:
#     chatbot.delete_all_conversations()
#     print("All conversations removed successfully.")
# except Exception as e:
#     print(e)

cookie_path_dir = "./cookies/"

class GenRequest(BaseModel):
    query: str
    email: str
    password: str

@app.post("/")
def generate_breakdown(request: GenRequest):

    sign = Login(request.email, request.password)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    chatbot.new_conversation(switch_to=True, system_prompt=system_prompt)
    
    try:
        print("Generating breakdown...")
        message = chatbot.chat(request.query).wait_until_done()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing the query: {e}")

    return JSONResponse({"breakdown": message})


# import time
# @app.post("/")
# def generate_breakdown(request: GenRequest):
#     print("hi")
#     time.sleep(3)
#     print("bye")
