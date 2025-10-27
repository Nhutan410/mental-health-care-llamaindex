"""
Setup script to create necessary directories
"""

import os

# Directories to create
directories = [
    "data/cache",
    "data/images",
    "data/index_storage",
    "data/ingestion_storage",
    "data/user_storage",
    "eval_results"
]


def setup_directories():
    """Create all necessary directories"""
    print("Setting up directories...")

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")

    # Create empty JSON files
    empty_files = {
        "data/user_storage/scores.json": "[]",
        "data/user_storage/users.yaml": ""
    }

    for filepath, content in empty_files.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created: {filepath}")

    print("\n✓ All directories and files created successfully!")
    print("\nNext steps:")
    print("1. Add your DSM-5 document to: data/ingestion_storage/")
    print("2. Update .streamlit/secrets.toml with your OpenAI API key")
    print("3. Run: python build_data.py")
    print("4. Run: streamlit run Home.py")


if __name__ == "__main__":
    setup_directories()
