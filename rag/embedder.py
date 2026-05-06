

from langchain_openai import OpenAIEmbeddings

from config import OPENAI_API_KEY


class Embedder:

    _instance = None

    @staticmethod
    def get_instance():
        if Embedder._instance is None:

            Embedder._instance = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=OPENAI_API_KEY
            )
        
        return Embedder._instance