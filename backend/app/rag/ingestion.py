import os
import json
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, WebBaseLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_store import get_vector_store

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "raw")

def load_all_documents():
    if not os.path.exists(DATA_DIR):
        print(f"Data directory {DATA_DIR} does not exist.")
        return []
        
    docs = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            domain = "university"
            
            try:
                if ext == ".pdf":
                    loader = PyPDFLoader(file_path)
                    loaded_docs = loader.load()
                    for d in loaded_docs: d.metadata["domain"] = domain
                    docs.extend(loaded_docs)
                elif ext == ".csv":
                    loader = CSVLoader(file_path)
                    loaded_docs = loader.load()
                    for d in loaded_docs: d.metadata["domain"] = domain
                    docs.extend(loaded_docs)
                elif ext == ".docx":
                    loader = Docx2txtLoader(file_path)
                    loaded_docs = loader.load()
                    for d in loaded_docs: d.metadata["domain"] = domain
                    docs.extend(loaded_docs)
                elif ext == ".json":
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                text_content = json.dumps(item, indent=2)
                                docs.append(Document(page_content=text_content, metadata={"source": file_path, "domain": domain}))
                        elif isinstance(data, dict):
                            text_content = json.dumps(data, indent=2)
                            docs.append(Document(page_content=text_content, metadata={"source": file_path, "domain": domain}))
                elif ext == ".txt":
                    if "links" in root.lower() or "link" in file.lower():
                        with open(file_path, 'r', encoding='utf-8') as f:
                            urls = [line.strip() for line in f if line.strip() and line.strip().startswith("http")]
                        if urls:
                            loader = WebBaseLoader(urls)
                            loaded_docs = loader.load()
                            for d in loaded_docs: d.metadata["domain"] = domain
                            docs.extend(loaded_docs)
                    else:
                        loader = TextLoader(file_path)
                        loaded_docs = loader.load()
                        for d in loaded_docs: d.metadata["domain"] = domain
                        docs.extend(loaded_docs)
            except Exception as e:
                print(f"Error loading {file}: {e}")
                
    return docs

def ingest_data():
    all_docs = load_all_documents()
        
    if not all_docs:
        print("No documents found to ingest.")
        return
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    vector_store = get_vector_store()
    vector_store.add_documents(splits)
    print(f"Ingested {len(splits)} chunks into ChromaDB.")

if __name__ == "__main__":
    ingest_data()
