"""
Global settings and configuration for the Mental Health Care System
"""

# Cache and storage paths
CACHE_FILE = "data/cache/pipeline_cache.json"
CONVERSATION_FILE = "data/cache/chat_history.json"

# Data paths
STORAGE_PATH = "data/ingestion_storage/"
FILES_PATH = ["data/ingestion_storage/dsm5.docx"]

# Index storage
INDEX_STORAGE = "data/index_storage"

# User data
SCORES_FILE = "data/user_storage/scores.json"
USERS_FILE = "data/user_storage/users.yaml"

# Application settings
APP_TITLE = "Hệ thống Chăm sóc Sức khỏe Tinh thần"
APP_ICON = "🧠"

# Model settings
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.2
CHUNK_SIZE = 512
CHUNK_OVERLAP = 20
SIMILARITY_TOP_K = 3