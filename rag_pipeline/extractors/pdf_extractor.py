import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            "page_number": page_num + 1,
            "text": text,
            "source": pdf_path
        })
    doc.close()
    return {"total_pages": len(pages), "pages": pages}

if __name__ == "__main__":
    result = extract_text_from_pdf("syllabus.pdf")
    print(f"Total pages: {result['total_pages']}")
   
    # Quick check: print first 100 chars of every page
    for p in result["pages"]:
        preview = p["text"].strip()[:80].replace("\n", " ")
        print(f"Page {p['page_number']}: {preview}")