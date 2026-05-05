# test_groq.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": "Balas dengan kata OK saja"}],
        max_tokens=10
    )
    print("✅ Groq aktif! Response:", response.choices[0].message.content)
except Exception as e:
    print("❌ Error:", e)