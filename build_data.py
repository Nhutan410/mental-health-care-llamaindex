"""
Build data pipeline - Create nodes and indexes
"""

from src.index_builder import build_indexes
from src.ingest_pipeline import ingest_documents, initialize_settings
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main function to build data"""
    print("=" * 50)
    print("Building Mental Health Care System Data")
    print("=" * 50)

    # Initialize settings
    print("\n[1/3] Initializing settings...")
    initialize_settings()
    print("✓ Settings initialized")

    # Create nodes
    print("\n[2/3] Processing documents and creating nodes...")
    nodes = ingest_documents()
    print(f"✓ Created {len(nodes)} nodes")

    # Build indexes
    print("\n[3/3] Building indexes...")
    index = build_indexes(nodes)
    print("✓ Indexes built successfully")

    print("\n" + "=" * 50)
    print("Data building completed successfully!")
    print("=" * 50)
    print("\nYou can now run the application with:")
    print("  streamlit run Home.py")


if __name__ == "__main__":
    main()
