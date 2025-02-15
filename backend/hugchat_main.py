from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from system_prompt import system_prompt
from hugchat import hugchat
from hugchat.login import Login
import docker
import json
import re

app = FastAPI()

cookie_path_dir = "./cookies/"

client = docker.from_env()

pg = client.containers.get("ichiran-pg-1")
pg.start()

main = client.containers.get("ichiran-main-1")
main.start()

def clean_input(text):
    text = "".join(text.split(" "))
    return re.sub(r"[^\w\sぁ-んァ-ン一-龥]", "", text)

def get_breakdown(text):
    exit_code, output = main.exec_run(f'ichiran-cli -f "{clean_input(text)}"')
    breakdowns = []

    if exit_code != 0:
        return exit_code, breakdowns

    output = output.decode("utf-8")
    output = "\n".join(line for line in output.splitlines() if not re.search(r"WARNING", line))
    output = json.loads(output)[0][0][0]

    for breakdown in output:
        word_data = breakdown[1]  # Get word info
        entry = {}
        components = []

        if "components" in word_data:
            components.extend(word_data["components"])

        if "alternative" in word_data:
            components.extend(word_data["alternative"])

        main_text = word_data.get("text")
        if not main_text and components:
            main_text = components[0].get("text", "UNKNOWN")  # Use first child's text

        if components:
            component_entries = []

            for component in components:
                word_entry = {component["text"]: []}

                if "gloss" in component:
                    for definition in component["gloss"]:
                        word_entry[component["text"]].append(definition["gloss"])

                elif "conj" in component and component["conj"]:
                    for conj in component["conj"]:
                        for gloss in conj.get("gloss", []):
                            word_entry[component["text"]].append(gloss["gloss"])

                elif "suffix" in component:
                    word_entry[component["text"]].append(component["suffix"])

                component_entries.append(word_entry)

            entry[f"{main_text}"] = component_entries

        else:
            word_entry = {main_text: []}

            if "gloss" in word_data:
                for definition in word_data["gloss"]:
                    word_entry[main_text].append(definition["gloss"])

            elif "conj" in word_data and word_data["conj"]:
                for conj in word_data["conj"]:
                    for gloss in conj.get("gloss", []):
                        word_entry[main_text].append(gloss["gloss"])

            entry[f"{main_text}"] = [word_entry]

        breakdowns.append(entry)

    return exit_code, breakdowns


class GenRequest(BaseModel):
    query: str
    email: str
    password: str
    breakdown_type: str

@app.post("/")
def generate_breakdown(request: GenRequest):
    print(f"Generating breakdown for {request.query} {request.breakdown_type}")
    if request.breakdown_type == "ichiran":
        exit_code, breakdowns = get_breakdown(request.query)
        if exit_code == 0:
            return JSONResponse(status_code=200, content={"breakdown": breakdowns})
        else:
            print(f"Exit code: {exit_code}, exit code != 0")
            return JSONResponse(status_code=500, content={"breakdown": "error"})
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
