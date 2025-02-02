from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from system_prompt import system_prompt
from hugchat import hugchat
from hugchat.login import Login
import docker
import json

app = FastAPI()

cookie_path_dir = "./cookies/"

client = docker.from_env()

pg = client.containers.get("ichiran-pg-1")
pg.start()

main = client.containers.get("ichiran-main-1")
main.start()

class GenRequest(BaseModel):
    query: str
    email: str
    password: str

@app.post("/")
def generate_breakdown(request: GenRequest):
    if request.breakdown_type == "ichiran":
        exit_code, output = main.exec_run(f'ichiran-cli -f "{request.query}"')
        try:
            assert(exit_code == 0)
            output = json.loads(output.decode())[0][0][0]
            breakdowns = [[breakdown[1]["reading"], breakdown[1]["gloss"]] for breakdown in output]
            print(breakdowns)
            return JSONResponse(status_code=200, content={"breakdown": breakdowns})
        except:
            print(output)
            return JSONResponse(status_code=500, content={"breakdown": "Ichiran generation failed"})
    else:
        try:
            sign = Login(request.email, request.password)
            cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            llm = 3
            chatbot.switch_llm(llm)
            chatbot.new_conversation(switch_to=True, system_prompt=system_prompt)
            print(f"Generating breakdown via {chatbot.get_available_llm_models()[llm].__dict__["name"]}")

            message = chatbot.chat(request.query).wait_until_done()
            return JSONResponse(status_code=200, content={"breakdown": message})
        except Exception as e:
            print({"breakdown": str(e)})
            return JSONResponse(status_code=500, content={"breakdown": str(e)})
