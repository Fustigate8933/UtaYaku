import litserve as ls
from model import Qwen32BInstruct

if __name__ == "__main__":
    api = Qwen32BInstruct()
    server = ls.LitServer(
        api,
        spec=ls.OpenAISpec(),
        timeout=30
    )
    server.run(generate_client_file=False)
