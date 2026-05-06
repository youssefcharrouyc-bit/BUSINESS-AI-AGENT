import os

from langchain_chroma import Chroma
from config import BASE_DIR
from rag.embedder import Embedder
from rag.embedder import Embedder

DB_PATH = os.path.join(BASE_DIR, 'vector_db_chroma')

if not os.path.exists(DB_PATH):
    print("Database directory does not exist.")
    exit()

print('Inspecting database at:', DB_PATH)

db = Chroma(persist_directory=DB_PATH, embedding_function=Embedder.get_instance())

try:
    data = db.get(include=['embeddings', 'documents'])

    for i, (text, vector) in enumerate(zip(data['documents'], data['embeddings'])):
        preview = text[:120].replace("\n", " ")
        print(f"CHUNK {i + 1}")
        print(f"Text Preview: {preview}...")
        print("Vector:", vector)
        print("-" * 40)
    print('DONE')

except Exception as e:
    print("Error loading database:", str(e))
    exit()