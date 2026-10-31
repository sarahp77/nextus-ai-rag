import os
import chromadb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()


embedding_client = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="NextusAI_docs")


def index_document(file_path: str = "knowledge_base.txt"):
    """It reads the text, chunks it, and stores the vectors in the database."""
   
    if collection.count() > 0:
        return f"Database already indexed with {collection.count()} chunks."

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

   
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50, separator="\n")
    chunks = splitter.split_text(raw_text)

   
    for i, chunk in enumerate(chunks):
        vector = embedding_client.embed_query(chunk)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[vector],
            documents=[chunk]
        )

    return f"Successfully indexed {len(chunks)} chunks into ChromaDB."


def search_knowledge(query: str, n_results: int = 2) -> str:
    """Searching for semantic similarity to find the text closest to the user's question."""
    query_vector = embedding_client.embed_query(query)
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )
    
    
    matched_docs = results.get("documents", [[]])[0]
    return "\n\n".join(matched_docs)
