import chromadb
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

client_chroma = chromadb.PersistentClient(path="chroma_db")

collection = client_chroma.get_collection(
    name="college_documents"
)


def generate_answer(question):

    query_embedding = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    results = collection.query(
        query_embeddings=[query_embedding.embeddings[0].values],
        n_results=3
    )

    if not results["documents"] or not results["documents"][0]:
        return {
            "answer": "Information not found in the provided documents.",
            "sources": []
        }

    documents = results["documents"][0]
    metadata = results["metadatas"][0]

    context = ""

    for i, doc in enumerate(documents):
        context += f"Context {i+1}:\n{doc}\n\n"

    prompt = f"""
You are a college information assistant.

Answer ONLY using the provided context.

If the answer is not available, reply:
Information not found in the provided documents.

Context:
{context}

Question:
{question}
"""

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sources = list(set(meta["source"] for meta in metadata))

    return {
        "answer": response.text,
        "sources": sources
    }
    
