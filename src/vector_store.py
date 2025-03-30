from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb
from llama_index.legacy.vector_stores.chroma import ChromaVectorStore
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class VectorStoreManager:
    def __init__(self):
        self.vector_store_dir = os.getenv('VECTOR_STORE_DIR', './vector_store')
        os.makedirs(self.vector_store_dir, exist_ok=True)
        
        # Use OpenAI embeddings
        self.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small", 
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient(path=self.vector_store_dir)
        self.collection = self.chroma_client.get_or_create_collection("documents")
        
        # Initialize vector store
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection)
        
        # Initialize storage context
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            vector_store=self.vector_store,
            index_store=SimpleIndexStore()
        )
        
        try:
            self.index = load_index_from_storage(
                storage_context=self.storage_context
            )
            print("Loaded existing vector index")
        except Exception as e:
            print(f"Creating new index: {str(e)}")
            self.index = VectorStoreIndex.from_documents(
                [], 
                storage_context=self.storage_context,
                embed_model=self.embed_model
            )
    
    def add_document(self, content: str, metadata: dict) -> str:
        """Add a document to the vector store and return its ID."""
        doc = Document(text=content, metadata=metadata)
        doc_id = self.index.insert(doc)
        return doc_id
    
    def search_similar(self, query: str, k: int = 5) -> List[dict]:
        """Search for similar documents."""
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query)
        
        results = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes[:k]:
                results.append({
                    'content': node.node.text,
                    'metadata': node.node.metadata,
                    'score': node.score if hasattr(node, 'score') else None
                })
        
        return results 