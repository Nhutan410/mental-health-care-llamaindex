"""
Index builder for creating and loading vector store indexes
"""

from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from src.global_settings import INDEX_STORAGE


def build_indexes(nodes):
    """
    Build or load vector store indexes
    
    Args:
        nodes: List of processed nodes
        
    Returns:
        VectorStoreIndex: The vector index
    """
    try:
        # Try to load existing index
        storage_context = StorageContext.from_defaults(
            persist_dir=INDEX_STORAGE
        )
        vector_index = load_index_from_storage(
            storage_context, 
            index_id="vector"
        )
        print("All indices loaded from storage.")
        
    except Exception as e:
        print(f"Error occurred while loading indices: {e}")
        print("Creating new indexes...")
        
        # Create new index
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(
            nodes, 
            storage_context=storage_context
        )
        vector_index.set_index_id("vector")
        
        # Persist the index
        storage_context.persist(persist_dir=INDEX_STORAGE)
        print("New indexes created and persisted.")
    
    return vector_index


if __name__ == "__main__":
    # Test index building
    from src.ingest_pipeline import ingest_documents, initialize_settings
    
    initialize_settings()
    nodes = ingest_documents()
    index = build_indexes(nodes)
    print("Index built successfully!")