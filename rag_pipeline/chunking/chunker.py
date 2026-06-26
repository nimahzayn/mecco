import json
import os

def chunk_text(text: str, source: str, source_type: str = "unknown",
               chunk_size: int = 400, overlap: int = 50) -> list[dict]:
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_str = " ".join(chunk_words)

        if len(chunk_words) > 20:  # skip tiny trailing chunks
            chunks.append({
                "chunk_id": f"{source}_{chunk_id}",
                "text": chunk_str,
                "source": source,
                "source_type": source_type,
                "word_count": len(chunk_words)
            })
            chunk_id += 1

        if end == len(words):
            break
        start += chunk_size - overlap

    return chunks


def chunk_documents(docs: list[dict], chunk_size: int = 400, overlap: int = 50) -> list[dict]:
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(
            doc["text"],
            source=doc.get("source", "unknown"),
            source_type=doc.get("source_type", "unknown"),
            chunk_size=chunk_size,
            overlap=overlap
        )
        all_chunks.extend(chunks)
    return all_chunks


if __name__ == "__main__":
    input_path = os.path.join("..", "processing", "cleaned_corpus.json")
    with open(input_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    chunks = chunk_documents(docs)

    print(f"Total documents: {len(docs)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Avg words/chunk: {sum(c['word_count'] for c in chunks) / len(chunks):.0f}")

    print("\n--- Sample chunk ---")
    print(chunks[0])

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print("\nSaved to chunks.json")