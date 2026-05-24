import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config import Config

class VectorStoreManager:
    def __init__(self):
        """
        Initializes the Vector Database layer using OpenAI Embeddings.
        """
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.db_path = "faiss_index"

    def create_and_save_index(self, texts: list[str]):
        """
        Takes raw source texts (e.g., peer-reviewed reference texts), 
        creates vector embeddings, and saves them locally.
        """
        if not texts:
            return
        
        vector_db = FAISS.from_texts(texts, self.embeddings)
        vector_db.save_local(self.db_path)
        print(f"Successfully built and saved FAISS index to {self.db_path}")

    def similarity_search(self, query: str, k: int = 3) -> list[str]:
        """
        Searches the vector store for context matching the query 
        to help the RAG Agent validate claims.
        """
        if not os.path.exists(self.db_path):
            print("Warning: Vector index directory not found. Returning empty context.")
            return []
            
        vector_db = FAISS.load_local(
            self.db_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        docs = vector_db.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
