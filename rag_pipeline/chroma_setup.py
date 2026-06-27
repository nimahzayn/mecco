import json
import chromadb
from google import genai

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

client_chroma = chromadb.PersistentClient(path="chroma_db")

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

collection = client_chroma.get_or_create_collection(
    name="college_documents"
)

documents = []
ids = []
metadata = []

for chunk in chunks:
    documents.append(chunk["text"])
    ids.append(chunk["chunk_id"])

    metadata.append({
        "source": chunk["source"],
        "source_type": chunk["source_type"]
    })

embeddings = []

for doc in documents:
    response = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=doc
    )

    embeddings.append(response.embeddings[0].values)

collection.upsert(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadata
)

print("Stored successfully!")
