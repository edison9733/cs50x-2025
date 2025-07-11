import os
from dotenv import load_dotenv
from openai import OpenAI  # Fixed import

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt
system_prompt = "You are a helpful assistant. Please answer the user's questions to the best of your ability."

# User input
user_prompt = input("Enter your message: ")

# Generate response
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    model="gpt-4o"  # Updated model name
)

# Print response
print(chat_completion.choices[0].message.content)
