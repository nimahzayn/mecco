import re

def clean_text(text: str) -> str:
    """Clean extracted text for RAG use."""
    # Remove common JS/noscript boilerplate
    text = re.sub(
        r'You need to enable JavaScript to run this app\.?',
        ' ', text, flags=re.IGNORECASE
    )

    # Remove page numbers like "Page 1 of 10" or "- 2 -"
    text = re.sub(r'-?\s*\d+\s*-?\s*(of\s*\d+)?\s*\n', ' ', text)

    # Collapse multiple whitespace/newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # Fix hyphenated words broken across lines
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    # Final whitespace collapse
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


def clean_documents(docs: list[dict]) -> list[dict]:
    """Apply cleaning to a list of extracted documents (from PDF or web)."""
    cleaned = []
    for doc in docs:
        text = doc.get("text", "")
        cleaned_text = clean_text(text)
        if len(cleaned_text) < 20:  # skip near-empty docs
            print(f"⚠ Skipping near-empty doc: {doc.get('source')}")
            continue
        new_doc = dict(doc)
        new_doc["text"] = cleaned_text
        cleaned.append(new_doc)
    return cleaned


if __name__ == "__main__":
    import json
    import os
    import sys

    sys.path.append(os.path.join("..", "extractors"))
    from pdf_extractor import extract_text_from_pdf

    all_docs = []

    # 1. Load and clean web data
    web_path = os.path.join("..", "extractors", "web_data.json")
    with open(web_path, "r", encoding="utf-8") as f:
        web_docs = json.load(f)
    all_docs.extend(web_docs)

    # 2. Load and clean PDF data (edit path to your actual PDF)
    pdf_path = os.path.join("..", "extractors", "syllabus.pdf")
    pdf_result = extract_text_from_pdf(pdf_path)
    for page in pdf_result["pages"]:
        all_docs.append({
            "text": page["text"],
            "source": f"{pdf_path} (page {page['page_number']})",
            "source_type": "pdf"
        })

    # 3. Clean everything together
    cleaned = clean_documents(all_docs)

    print(f"Cleaned {len(cleaned)}/{len(all_docs)} documents total")
    print(f"  Web docs: {len(web_docs)}")
    print(f"  PDF pages: {len(pdf_result['pages'])}")

    with open("cleaned_corpus.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    print("\nSaved combined corpus to cleaned_corpus.json")