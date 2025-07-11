import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = "You are a helpful assistant. Please answer the user\'s questions to the best of your ability."

user_prompt = input("Enter your message: ")

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    model="gpt-4.0",
)

response_text = chat_completion.choices[0].message.content

print(response_text)
