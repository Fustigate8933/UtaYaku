from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import json
import re

app = FastAPI()

# Ichiran CLI command
cmd = ["/home/fustigate/quicklisp/local-projects/ichiran/ichiran-cli", "-f", "-l", "5"]

def clean_input(text):
    text = "".join(text.split(" "))
    return re.sub(r"[^\w\sぁ-んァ-ン一-龥]", "", text)

async def get_breakdown(text):
    """Runs ichiran-cli asynchronously and returns parsed JSON output."""
    process = await asyncio.create_subprocess_exec(
        *cmd, clean_input(text),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        return {"error": f"Failed for {text}"}

    output = stdout.decode("utf-8")
    output = "\n".join(line for line in output.splitlines() if not re.search(r"WARNING", line))

    try:
        output = json.loads(output)[0][0][0]
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON output for {text}"}

    breakdowns = []
    for breakdown in output:
        word_data = breakdown[1]
        entry = {}
        components = word_data.get("components", []) + word_data.get("alternative", [])

        main_text = word_data.get("text") or (components[0]["text"] if components else "UNKNOWN")

        if components:
            component_entries = []
            for component in components:
                word_entry = {component["text"]: []}
                if "gloss" in component:
                    for definition in component["gloss"]:
                        word_entry[component["text"]].append(definition["gloss"])
                elif "conj" in component:
                    for conj in component["conj"]:
                        for gloss in conj.get("gloss", []):
                            word_entry[component["text"]].append(gloss["gloss"])
                elif "suffix" in component:
                    word_entry[component["text"]].append(component["suffix"])
                component_entries.append(word_entry)

            entry[main_text] = component_entries
        else:
            word_entry = {main_text: []}
            if "gloss" in word_data:
                for definition in word_data["gloss"]:
                    word_entry[main_text].append(definition["gloss"])
            elif "conj" in word_data:
                for conj in word_data["conj"]:
                    for gloss in conj.get("gloss", []):
                        word_entry[main_text].append(gloss["gloss"])
            entry[main_text] = [word_entry]

        breakdowns.append(entry)

    return breakdowns

class GenRequest(BaseModel):
    queries: list[str]  # 🔹 Accept multiple sentences
    breakdown_type: str
    email: str
    password: str

@app.post("/")
async def generate_breakdowns(request: GenRequest):
    if request.breakdown_type != "ichiran":
        return JSONResponse(status_code=400, content={"error": "Invalid breakdown type"})

    print(f"Processing {len(request.queries)} queries in parallel...")

    # Run all queries in parallel and return just the breakdowns
    results = await asyncio.gather(*(get_breakdown(query) for query in request.queries))

    return JSONResponse(status_code=200, content=results)

