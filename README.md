# UtaYaku
Learn Japanese with music. Just like Spotify and other music services, read the auto-scrolling lyrics as you listen. When you encounter new vocabulary or grammar or just want to understand what the sentence means, click on the lyric to access the definitions and breakdown of the sentence into its components and grammar. Login to save your song (not yet developed).

I plan to support **playlist importing** from music services like Spotify and Youtube Music. I also plan on turning it into an app since most people use their phones for music.

The lyric breakdown uses HuggingChat.

This is a preview of the current state:

https://github.com/user-attachments/assets/3ff5f303-2407-41ce-b273-667401342ed4


#### Installation
1. Clone the repository and cd into it
2. Run `pnpm install` or `npm install` or the equivalent whatever package manager you prefer.
3. Create a .env file in the root directory with `CLIENT_ID=<your client id from app.musicapi.com>`, which can be found at [apiAccess](https://app.musicapi.com/admin/account/apiAccess).
4. Register for an account on HuggingChat.
5. pnpm run dev
6. access the website on http://localhost:3000/
