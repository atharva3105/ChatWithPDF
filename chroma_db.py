import os
import openai
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
os.getenv("TOGETHER_API_KEY")

# Initialize ChromaDB client
db_folder = "ChromaDB_Data"
collection_name = "pdf_database"
if not os.path.exists(db_folder):
    os.makedirs(db_folder)
Chromaclient = chromadb.PersistentClient(path=db_folder)

# Create OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
)

def get_collection():
    if collection_name not in [col.name for col in Chromaclient.list_collections()]:
        collection = Chromaclient.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    else:
        collection = Chromaclient.get_collection(name=collection_name)
    return collection

def get_embeddings(chunks):
    response = client.embeddings.create(
        model="togethercomputer/m2-bert-80M-8k-retrieval",
        input=chunks
    )
    response_dict = response.to_dict()
    embeddings = [item['embedding'] for item in response_dict['data']]
    return embeddings

def store_embeddings_chroma(chunks_with_metadata):
    collection = get_collection()

    chunks = [chunk_info["chunk"] for chunk_info in chunks_with_metadata]
    metadatas = [
        {
            "pdf_num": chunk_info["pdf_num"],
            "chunk_num": chunk_info["chunk_num"],
            "start_index": chunk_info["start_index"]
        }
        for chunk_info in chunks_with_metadata
    ]

    embeddings = get_embeddings(chunks=chunks)
    ids = [f"{metadata['pdf_num']}-{metadata['chunk_num']}" for metadata in metadatas]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_db(question):
    collection = get_collection()
    embedding = get_embeddings(question)
    results = collection.query(
        query_embeddings=embedding,
        n_results=5
    )
    context = ""
    for c in results['documents']:
        context += str(c) + "\n"

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
        messages=[
            {"role": "user", "content": f"""
            {context}
            - -
            Answer the question based on the above context: {question}
            """},
        ]
    )
    message_content = response.choices[0].message.content
    return message_content
    

def delete_previous_data():
    collection = get_collection()
    Chromaclient.delete_collection(collection_name)
