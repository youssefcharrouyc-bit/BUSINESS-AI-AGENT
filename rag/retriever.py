
from .vector_store import VectorStore


class RAGRetriever:
    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, k: int=5) -> str:
        """
        Retrieve top-k relevant documents for the given query.
        """

        docs = self.vector_store.similarity_search(query, k=k)


        if not docs:
            return ""
        
        # Format chunks
        formatted_chunks = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "?")
            formatted_chunks.append(
                f"---CHUNK {i} (Source: {source}, Page: {page}) ---\n{doc.page_content}"
            )

        return "\n\n".join(formatted_chunks)