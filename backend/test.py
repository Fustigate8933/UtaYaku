import docker
import json

client = docker.from_env()

pg = client.containers.get("ichiran-pg-1")
pg.start()

main = client.containers.get("ichiran-main-1")
main.start()

exit_code, output = main.exec_run('ichiran-cli -f "今日は楽しかったな"')

# the output is returned as bytes so we have to decode it into string and use json.loads() to turn it into an array
output = json.loads(output.decode())[0][0][0]
reading = output[0][1]["reading"]
definitions = output[0][1]["gloss"]

print(f"{reading}: {definitions}")
