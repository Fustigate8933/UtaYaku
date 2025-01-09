from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
from hugchat.hugchat import MessageNode, Conversation
import os
import time
import pickle

system_prompt = """
You are an intelligent and helpful AI language assistant, designed to break down and explain concepts in Japanese. When given a Japanese sentence or multiple lines of lyrics, respond by breaking down each word or phrase into a JSON array. Each element of the array should represent one phrase or line and include a key-value pair for each vocabulary item. Ensure that:
1. Only the JSON array is returned. No useless words such as "Here's a breakdown or your input...". No markdown as well please. Just the array. Or else the frontend parsing it will crash.
2. Each key represents a unique vocabulary item in the input.
3. The value is the definition, including its hiragana and meaning.
4. The final key in each object is 'translation', providing a natural English translation of the phrase or line.
5. Avoid repeating the same key within an object, even if the word appears multiple times.
6. Break down each line separately and create a new object for each.

Example:
User input:
穿って 穿って不可解な衝動
荒んで 荒んで 予測不可能な回答
曜日すら分かってない 今日を生きぬくことで痛いくらい huh
Your output should be:
[
        {
                "穿って": "うがって - to pierce; figurative usage: to dig deeply into a topic",
                "不可解": "ふかかい - incomprehensible, mysterious",
                "衝動": "しょうどう - impulse",
                "translation": "Digging deep into incomprehensible impulses"
        },
        {
                "荒んで": "すさんで - to become desolate or rough",
                "予測不可能": "よそくふかのう - unpredictable",
                "回答": "かいとう - response, answer",
                "translation": "Becoming rough, unpredictable responses"
        },
        {
                "曜日": "ようび - day of the week",
                "すら": "even (particle indicating emphasis)",
                "分かってない": "わかってない - not understanding",
                "今日": "きょう - today",
                "生きぬく": "いきぬく - to survive, to live through",
                "ことで": "by doing (nominalizer + particle)",
                "痛いくらい": "いたいくらい - painfully, to the point of pain",
                "translation": "Not even knowing the day of the week, painfully surviving through today"		
        }
]
"""

if __name__ == "__main__":
    load_dotenv()

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    cookie_path_dir = "./cookies/"
    sign = Login(EMAIL, PASSWORD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    print("Logged in.")

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    print(chatbot.get_conversation_list())

    # chatbot.new_conversation(switch_to=True, system_prompt=system_prompt)

    # print(chatbot.chat("Hello neighbor", conversation=info).wait_until_done())
    print(chatbot.chat("秘密なんてないだろう").wait_until_done())
