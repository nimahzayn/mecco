import json
from google import genai

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = []

for chunk in chunks:
    response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunk["text"]
    )
    embeddings.append(response.embeddings[0].values)

print(len(chunks))
print(len(embeddings[0]))
