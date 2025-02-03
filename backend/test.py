import docker
import json
import re
from pprint import pprint

client = docker.from_env()

# Start the required containers
pg = client.containers.get("ichiran-pg-1")
pg.start()

main = client.containers.get("ichiran-main-1")
main.start()

def clean_input(text):
    return re.sub(r"[^\w\sぁ-んァ-ン一-龥]", "", text)

query = "「らしくていいね」と笑いかけた"
exit_code, output = main.exec_run(f'ichiran-cli -f "{clean_input(query)}"')
output = output.decode("utf-8")
output = "\n".join(line for line in output.splitlines() if not re.search(r"WARNING", line))
output = json.loads(output)[0][0][0]

breakdowns = []

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

# Pretty print the final structured data
pprint(breakdowns, width=120)

