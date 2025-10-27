"""
Data ingestion pipeline for processing documents
"""

from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
import openai
import streamlit as st
from src.global_settings import (
    STORAGE_PATH,
    FILES_PATH,
    CACHE_FILE,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from src.prompts import CUSTORM_SUMMARY_EXTRACT_TEMPLATE


def initialize_settings():
    """Initialize OpenAI settings"""
    openai.api_key = st.secrets.openai.OPENAI_API_KEY
    Settings.llm = OpenAI(model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE)


def ingest_documents():
    """
    Load and process documents through ingestion pipeline

    Returns:
        list: Processed nodes
    """
    # Load documents with filename as ID
    documents = SimpleDirectoryReader(
        input_files=FILES_PATH,
        filename_as_id=True
    ).load_data()

    print(f"Loaded {len(documents)} documents")
    for doc in documents:
        print(f"Document ID: {doc.id_}")

    # Try to load cached pipeline
    try:
        cached_hashes = IngestionCache.from_persist_path(CACHE_FILE)
        print("Cache file found. Running using cache...")
    except:
        cached_hashes = ""
        print("No cache file found. Running without cache...")

    # Create ingestion pipeline
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            ),
            SummaryExtractor(
                summaries=['self'],
                prompt_template=CUSTORM_SUMMARY_EXTRACT_TEMPLATE
            ),
            OpenAIEmbedding()
        ],
        cache=cached_hashes
    )

    # Process documents
    nodes = pipeline.run(documents=documents)

    # Save cache
    pipeline.cache.persist(CACHE_FILE)
    print(f"Processed {len(nodes)} nodes and saved cache")

    return nodes


if __name__ == "__main__":
    # Test the pipeline
    initialize_settings()
    nodes = ingest_documents()
    print(f"Successfully created {len(nodes)} nodes")
