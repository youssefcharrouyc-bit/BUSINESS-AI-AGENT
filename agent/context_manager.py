

import io
from fastapi import UploadFile
import pypdf
from rag.vector_store import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore[import]

class ContextManager:

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_FILE_TYPES = ['application/pdf', 'text/plain']

    def __init__(self):
        self.vector_store = VectorStore()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

    async def ingest_file(self, file: UploadFile):

        # 1. Validation
        if file.content_type not in self.ALLOWED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {file.content_type}")
    
        content = await file.read()
        if len(content) > self.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds the limit of {self.MAX_FILE_SIZE} bytes.")
        
        # 2. Text Extraction
        raw_text = ""

        try:
            if file.content_type == "application/pdf":
                reader = pypdf.PdfReader(io.BytesIO(content))

                for i, page in enumerate(reader.pages):
                    text = page.extract_text()

                    if text:
                        raw_text += f"\n --- Page {i+1} ---\n{text}"
            else:
                raw_text = content.decode('utf-8')
        except:
            raise ValueError("Failed to extract text from the file.")

        
        # 3. Text Splitting
        chunks = self.splitter.create_documents(
            [raw_text],
            metadatas=[{"source": file.filename, "page": i + 1}]
        )    

        # 4. Store in vector database

        self.vector_store
        self.vector_store.add_documents(chunks)

        return len(chunks)