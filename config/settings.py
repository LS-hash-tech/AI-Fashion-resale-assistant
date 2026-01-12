"""
Configuration settings for GrabyAI Assistant
"""

# Rate limiting
RATE_LIMIT_REQUESTS = 10  # requests per time window
RATE_LIMIT_WINDOW = 60  # seconds

# Price validation
MIN_PRICE = 1
MAX_PRICE = 100000

# Model configuration
MODEL_NAME = "gpt-4o-mini"
MODEL_TEMPERATURE = 0.7
EMBEDDING_MODEL = "text-embedding-3-small"

# RAG configuration
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
SIMILARITY_SEARCH_K = 3

# Logging
LOG_FILE = "grabyai_assistant.log"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Platform info
PLATFORM_NAME = "Graby AI"
SUPPORT_EMAIL = "info@graby.ai"
WHATSAPP_GROUP_EMAIL = "info@graby.ai"
