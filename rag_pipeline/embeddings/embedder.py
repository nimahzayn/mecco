import json
import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = "multi-qa-MiniLM-L6-cos-v1"

def embed_chunks(chunks: list[dict], model: SentenceTransformer) -> list[dict]:
    """Add embedding vectors to each chunk."""
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    return chunks


if __name__ == "__main__":
    input_path = os.path.join("..", "chunking", "chunks.json")
    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loading model: {MODEL_NAME} (first run downloads it, may take a minute)")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Embedding {len(chunks)} chunks...")
    chunks_with_embeddings = embed_chunks(chunks, model)

    print(f"\nEmbedding dimension: {len(chunks_with_embeddings[0]['embedding'])}")

    with open("chunks_with_embeddings.json", "w", encoding="utf-8") as f:
        json.dump(chunks_with_embeddings, f)
    print("Saved to chunks_with_embeddings.json")
    