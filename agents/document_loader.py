import fitz  # PyMuPDF


def load_document(file_path):
    """
    Load PDF document and extract text.
    """

    print(f"\n[INFO] Opening PDF: {file_path}")

    try:
        doc = fitz.open(file_path)

        text = ""

        for page_num, page in enumerate(doc):
            print(f"[INFO] Reading page {page_num + 1}")

            text += page.get_text()

        doc.close()

        if not text.strip():
            raise ValueError("No text extracted from PDF.")

        print("[SUCCESS] PDF text extracted successfully.")

        return text

    except Exception as e:
        print(f"[ERROR] Failed to load PDF: {e}")
        raise