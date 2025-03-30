import pytest
import os
import shutil
from src.vector_store import VectorStoreManager

@pytest.fixture
def vector_store():
    # Set up test environment
    os.environ['VECTOR_STORE_DIR'] = './test_vector_store'
    
    # Create vector store
    store = VectorStoreManager()
    
    yield store
    
    # Cleanup
    shutil.rmtree('./test_vector_store', ignore_errors=True)

def test_add_and_search_document(vector_store):
    # Test document
    content = "This is a test document about artificial intelligence and machine learning."
    metadata = {"url": "http://test.com", "title": "Test Document"}
    
    # Add document
    doc_id = vector_store.add_document(content, metadata)
    assert doc_id is not None
    
    # Search for similar documents
    results = vector_store.search_similar("What is artificial intelligence?")
    assert len(results) > 0
    assert "artificial intelligence" in results[0]['content'].lower()
    assert results[0]['metadata']['url'] == "http://test.com" 