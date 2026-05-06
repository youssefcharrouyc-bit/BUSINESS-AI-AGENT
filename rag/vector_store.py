


from typing import List
import os
from config import BASE_DIR
from rag.embedder import Embedder
from langchain_chroma import Chroma
from langchain_core.documents import Document


class VectorStore:

    VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db_chroma")

    def __init__(self):
        self.embedding_function = Embedder.get_instance()

        self.db = Chroma(
            persist_directory=self.VECTOR_DB_DIR,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Document]):
        
        if not documents:
            return
        
        self.db.add_documents(documents)
        print(f"Added {len(documents)} documents to the vector store.")

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        
        return self.db.similarity_search(query, k=k)
    
    def clear(self):
        try:
            self.db.reset_collection()
            print("Vector store cleared successfully.")

        except Exception as e:
            print(f"Error clearing vector store: {e}")