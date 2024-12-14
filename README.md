# UtaYaku
You should change the model to fit your machine. After a lot of experimentation with lots of models locally (RTX 4080) I still would just prefer OpenAI models. It's much more accurate and a hell lot faster.

#### Installation
1. Clone the repository and cd into it
2. Run `pnpm install` or `npm install` or the equivalent whatever package manager you prefer.
3. Create a .env file in the root directory with `CLIENT_ID=<your client id from app.musicapi.com>`
4. add `OPENAI_API_KEY=<your openai key that supports gpt4-o` as an environment variable
5. cd into the backend directory and run `pip install -r requirements.txt`

#### Usage
1. `pnpm run dev`
2. on a separate shell in the backend directory, `python main.py`
3. access the website on http://localhost:3000/
