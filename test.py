import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

key = os.getenv("GROQ_API_KEY")

if not key:
    raise RuntimeError("GROQ_API_KEY was not loaded")

client = Groq(api_key=key)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Reply with: API works"}
    ],
)

print(response.choices[0].message.content)