from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text(pdf_files):
    text_with_metadata = []
    for pdf_num, pdf in enumerate(pdf_files):
        pdf_reader = PdfReader(pdf)
        full_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:  
                full_text += text
        if full_text:  
            text_with_metadata.append((full_text, pdf_num + 1))
    return text_with_metadata

def get_chunks(text_with_metadata):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks_with_metadata = []
    
    for text, pdf_num in text_with_metadata:
        chunks = text_splitter.split_text(text)
        chunk_num = 0
        start_index = 0
        
        for chunk in chunks:
            chunks_with_metadata.append({
                "chunk": chunk,
                "pdf_num": pdf_num,
                "chunk_num": chunk_num,
                "start_index": start_index
            })

            start_index += len(chunk) - 200
            chunk_num += 1

    return chunks_with_metadata
