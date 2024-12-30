# UtaYaku
Learn Japanese with music. Just like Spotify and other music services, read the auto-scrolling lyrics as you listen. When you encounter new vocabulary or grammar or just want to understand what the sentence means, click on the lyric to access the definitions and breakdown of the sentence into its components and grammar. Login to save your song.

I hoep to support **playlist importing** from music services like Spotify and Youtube Music. I also plan on turning it into an app since most people use their phones for music.

The lyric breakdown works through OpenAI api calls, currently, I'm only using my own key for development (There is a separate branch for running a local llm). I'm still thinking about how I'll pay if I deploy it once ready. I really wish to deploy it. Bur for now I'm adding a database to store already broken down lyrics for each unique song so that a call to the API won't be needed if visiting already broken down songs.

This is a preview of the current state:

https://github.com/user-attachments/assets/65531511-e706-4262-ba08-79011c40f367







#### Installation
1. Clone the repository and cd into it
2. Run `pnpm install` or `npm install` or the equivalent whatever package manager you prefer.
3. Create a .env file in the root directory with `CLIENT_ID=<your client id from app.musicapi.com>`, which can be found at [apiAccess](https://app.musicapi.com/admin/account/apiAccess).
4. add `OPENAI_API_KEY=<your openai key that supports gpt4-o` as an environment variable
5. pnpm run dev
6. access the website on http://localhost:3000/
