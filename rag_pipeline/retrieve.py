import chromadb
from google import genai

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

client_chroma = chromadb.PersistentClient(path="chroma_db")

collection = client_chroma.get_collection(
    name="college_documents"
)

while True:
    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    query_embedding = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.embeddings[0].values
        ],
        n_results=3
    )
    
    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    
    context = ""
    for i, doc in enumerate(documents):
        context += f"Context {i+1}:\n{doc}\n\n"

    prompt = f"""
    You are a college information assistant.

    Answer ONLY using the provided context.
    
    you can also answer basic questions which are part of the conversation like hi, hello, how are you and so on.

    If the answer is not available in the context, say:
    "Information not found in the provided documents."

    Context:
     {context}

    Question:
     {question}
    """

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nAnswer:")
    print(response.text)
    
