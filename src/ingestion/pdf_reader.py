import fitz
import os
def read_pdf(pdf_path):
    document_name = os.path.basename(pdf_path)
    pages=[]
    try:
        with fitz.open(pdf_path) as doc:
            for page_number in range(doc.page_count):
                page=doc.load_page(page_number)
                text=page.get_text()
                if text.strip():
                    pages.append({"document_name":document_name,"page_number":page_number+1,"text":text})
            return pages
    except Exception as e:
        print(f"Error: {e}")
        return pages
