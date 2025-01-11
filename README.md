# UtaYaku
Learn Japanese with music. Just like Spotify and other music services, read the auto-scrolling lyrics as you listen. When you encounter new vocabulary or grammar or just want to understand what the sentence means, click on the lyric to access the definitions and breakdown of the sentence into its components and grammar. Login to save your song.

I hope to support **playlist importing** from music services like Spotify and Youtube Music. I also plan on turning it into an app since most people use their phones for music.

The lyric breakdown works through AI api calls. The master branch uses OpenAI, which requires you to configure your own key, and the hugchat branch uses a free api from huggingface. Note: the latter is significantly slower.

This is a preview of the current state:

<img src="https://github.com/user-attachments/assets/43f9f226-f84d-45e1-81d0-9a2f824cd6e3" width="350">

https://github.com/user-attachments/assets/65531511-e706-4262-ba08-79011c40f367



#### Installation
1. Clone the repository and cd into it
2. Run `pnpm install` or `npm install` or the equivalent whatever package manager you prefer.
3. Create a .env file in the root directory with `CLIENT_ID=<your client id from app.musicapi.com>`, which can be found at [apiAccess](https://app.musicapi.com/admin/account/apiAccess).
4. add `OPENAI_API_KEY=<your openai key that supports gpt4-o` as an environment variable
5. pnpm run dev
6. access the website on http://localhost:3000/
