from llama_index.legacy import (
    Document, 
    VectorStoreIndex, 
    StorageContext,
)
from llama_index.legacy.indices.loading import load_index_from_storage
from llama_index.legacy.storage.docstore import SimpleDocumentStore
from llama_index.legacy.storage.index_store import SimpleIndexStore
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
        
        try:
            # Try to get existing collection
            self.collection = self.chroma_client.get_collection("documents")
            print("Found existing collection")
        except:
            # Create new collection if it doesn't exist
            self.collection = self.chroma_client.create_collection("documents")
            print("Created new collection")
        
        # Initialize vector store with the collection
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection)
        
        # Initialize storage context
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            vector_store=self.vector_store,
            index_store=SimpleIndexStore(),
            persist_dir=self.vector_store_dir
        )

        try:
            # Try to load existing index
            self.index = load_index_from_storage(
                storage_context=self.storage_context,
                embed_model=self.embed_model
            )
            print("Loaded existing vector index")
        except Exception as e:
            print(f"Creating new index: {str(e)}")
            # Create new index if loading fails
            documents = []  # Empty list of documents to start with
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context,
                embed_model=self.embed_model
            )
            # Persist the empty index
            self.index.storage_context.persist(persist_dir=self.vector_store_dir)
    
    def add_document(self, content: str, metadata: dict) -> str:
        """Add a document to the vector store and return its ID."""
        doc = Document(text=content, metadata=metadata)
        doc_id = self.index.insert(doc)
        # Persist after adding document
        self.index.storage_context.persist(persist_dir=self.vector_store_dir)
        return doc_id
    
    def search_similar(self, query: str, k: int = 5) -> List[dict]:
        """Search for similar documents."""
        query_engine = self.index.as_query_engine(similarity_top_k=k)
        response = query_engine.query(query)
        
        results = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                results.append({
                    'content': node.node.text,
                    'metadata': node.node.metadata,
                    'score': node.score if hasattr(node, 'score') else None
                })
        
        return results 